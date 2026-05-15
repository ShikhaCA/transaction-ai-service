from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import shutil
import time
import logging

from service import (
    get_transactions,
    generate_summary,
    generate_category_insights,
    generate_trend_analysis,
    generate_failure_analysis,
    ask_ai
)

from rag.embeddings.vector_store import (
    list_documents,
    delete_document
)

from rag.retrieval.retriever import retrieve_docs

from tasks import process_document


# ================================
# LOGGER
# ================================
logger = logging.getLogger(__name__)


# ================================
# FASTAPI APP
# ================================
app = FastAPI(
    title="AI Report Service"
)


# ================================
# CORS
# ================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================================
# REQUEST MODEL
# ================================
class ProcessRequest(BaseModel):
    file_path: str


# ================================
# HOME API
# ================================
@app.get("/")
def home():

    return {
        "message": "AI Report Service Running 🚀"
    }


# ================================
# INTERNAL DOCUMENT PROCESSING
# ================================
@app.post("/internal/process-document")
def internal_process_document(data: ProcessRequest):

    try:

        logger.info(
            f"Processing started for: {data.file_path}"
        )

        from rag.ingestion.loader import load_pdf
        from rag.ingestion.chunker import split_documents

        from rag.embeddings.vector_store import (
            store_embeddings
        )

        docs = load_pdf(data.file_path)

        chunks = split_documents(docs)

        store_embeddings(
            chunks,
            data.file_path
        )

        logger.info(
            f"Processing completed for: {data.file_path}"
        )

        return {
            "message": "Document processed successfully"
        }

    except Exception as e:

        logger.error(
            f"Processing error: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ================================
# AI SUMMARY
# ================================
@app.get("/reports/ai-summary/{user_id}")
def ai_summary(user_id: str):

    data = get_transactions(user_id)

    result = generate_summary(data)

    return {
        "user_id": user_id,
        "summary": result
    }


# ================================
# CATEGORY INSIGHTS
# ================================
@app.get("/reports/ai-category-insights/{user_id}")
def category(user_id: str):

    data = get_transactions(user_id)

    result = generate_category_insights(data)

    return {
        "user_id": user_id,
        "insights": result
    }


# ================================
# TREND ANALYSIS
# ================================
@app.get("/reports/ai-trend/{user_id}")
def trend(user_id: str):

    data = get_transactions(user_id)

    result = generate_trend_analysis(data)

    return {
        "user_id": user_id,
        "trend": result
    }


# ================================
# FAILURE ANALYSIS
# ================================
@app.get("/reports/ai-failures/{user_id}")
def failure(user_id: str):

    data = get_transactions(user_id)

    result = generate_failure_analysis(data)

    return {
        "user_id": user_id,
        "failures": result
    }


# ================================
# RAG UPLOAD WITH CELERY
# ================================
@app.post("/rag/upload")
def upload_doc(
    file: UploadFile = File(...)
):

    try:

        allowed_types = [
            "application/pdf",
            "text/plain",
            "text/csv"
        ]

        if file.content_type not in allowed_types:

            raise HTTPException(
                status_code=400,
                detail="Only PDF, TXT, CSV files are allowed"
            )

        file_path = f"temp_{file.filename}"

        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        logger.info(
            f"File uploaded: {file.filename}"
        )

        process_document.delay(file_path)

        return {
            "message": "File uploaded successfully. Task sent to worker queue."
        }

    except Exception as e:

        logger.error(
            f"Upload error: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ================================
# LIST DOCUMENTS
# ================================
@app.get("/rag/docs")
def get_rag_docs():

    docs = list_documents()

    return {
        "documents": docs
    }


# ================================
# DELETE DOCUMENT
# ================================
@app.delete("/rag/docs/{doc_id}")
def delete_rag_doc(doc_id: str):

    deleted = delete_document(doc_id)

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "message": "Document deleted successfully"
    }


# ================================
# RAG QUERY
# ================================
@app.post("/rag/query")
def query_doc(query: str):

    start_time = time.time()

    try:

        docs = retrieve_docs(query)

        if not docs:

            latency = round(
                time.time() - start_time,
                2
            )

            logger.info(
                f"RAG query completed in {latency} seconds"
            )

            return {
                "answer": "No relevant information found in documents",
                "sources": []
            }

        context = "\n".join([
            doc.page_content
            for doc in docs
        ])

        context = context[:2000]

        sources = list(set([
            doc.metadata.get(
                "source",
                "unknown"
            )
            for doc in docs
        ]))

        prompt = f"""
        You are an AI assistant.

        Answer ONLY using the context below.

        If answer is not present,
        say "Not available".

        Context:
        {context}

        Question:
        {query}
        """

        result = ask_ai(prompt)

        latency = round(
            time.time() - start_time,
            2
        )

        logger.info(
            f"RAG query completed in {latency} seconds"
        )

        return {
            "answer": result,
            "sources": sources
        }

    except Exception as e:

        logger.error(
            f"RAG query error: {str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
