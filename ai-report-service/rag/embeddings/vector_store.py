import re
import uuid
import weaviate

from weaviate.connect import ConnectionParams

from langchain_weaviate import WeaviateVectorStore
from langchain_huggingface import HuggingFaceEmbeddings


# ================================
# EMBEDDING MODEL
# ================================
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ================================
# WEAVIATE CLIENT
# ================================
client = weaviate.WeaviateClient(
    connection_params=ConnectionParams.from_url(
        url="http://weaviate:8080",
        grpc_port=50051
    )
)

client.connect()

INDEX_NAME = "TransactionDocs"


# ================================
# STORE DOCUMENTS
# ================================
uploaded_documents = []


# ================================
# CLEAN METADATA
# ================================
def clean_metadata(metadata):

    cleaned = {}

    for key, value in metadata.items():

        new_key = re.sub(
            r'[^A-Za-z0-9_]',
            '_',
            key
        )

        if not re.match(r'^[A-Za-z_]', new_key):
            new_key = f"field_{new_key}"

        cleaned[new_key] = str(value)

    return cleaned


# ================================
# STORE EMBEDDINGS
# ================================
def store_embeddings(chunks, filename="unknown"):

    for chunk in chunks:

        chunk.metadata = clean_metadata(
            chunk.metadata
        )

        chunk.metadata["document_name"] = filename


    WeaviateVectorStore.from_documents(
        documents=chunks,
        embedding=embedding_model,
        client=client,
        index_name=INDEX_NAME,
        text_key="text"
    )

    uploaded_documents.append({
        "id": str(uuid.uuid4()),
        "filename": filename
    })


# ================================
# LOAD VECTOR DATABASE
# ================================
def load_vector_db():

    vector_db = WeaviateVectorStore(
        client=client,
        index_name=INDEX_NAME,
        text_key="text",
        embedding=embedding_model
    )

    return vector_db


# ================================
# LIST DOCUMENTS
# ================================
def list_documents():

    return uploaded_documents


# ================================
# DELETE DOCUMENT
# ================================
def delete_document(doc_id):

    global uploaded_documents

    for doc in uploaded_documents:

        if doc["id"] == doc_id:

            uploaded_documents = [
                d for d in uploaded_documents
                if d["id"] != doc_id
            ]

            return True

    return False
