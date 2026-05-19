import os
import re
import uuid
import weaviate

from weaviate.classes.init import Auth

from langchain_weaviate import WeaviateVectorStore
from langchain_huggingface import HuggingFaceEmbeddings


# ================================
# EMBEDDING MODEL
# ================================
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ================================
# WEAVIATE CONFIG
# ================================
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")


# ================================
# WEAVIATE CLIENT
# ================================
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,
    auth_credentials=Auth.api_key(
        WEAVIATE_API_KEY
    )
)


# ================================
# COLLECTION NAME
# ================================
INDEX_NAME = "TransactionDocs"


# ================================
# DOCUMENT STORE
# ================================
uploaded_documents = []


# ================================
# CLEAN METADATA
# ================================
def clean_metadata(metadata):

    cleaned = {}

    for key, value in metadata.items():

        # REMOVE INVALID CHARACTERS
        new_key = re.sub(
            r"[^A-Za-z0-9_]",
            "_",
            key
        )

        # ENSURE VALID START CHARACTER
        if not re.match(r"^[A-Za-z_]", new_key):
            new_key = f"field_{new_key}"

        cleaned[new_key] = str(value)

    return cleaned


# ================================
# CREATE COLLECTION IF NOT EXISTS
# ================================
def create_collection():

    existing = client.collections.list_all()

    if INDEX_NAME not in existing:

        client.collections.create(
            name=INDEX_NAME
        )

        print(f"\nCollection created: {INDEX_NAME}")

    else:

        print(f"\nCollection already exists: {INDEX_NAME}")


# CREATE COLLECTION ON STARTUP
create_collection()


# ================================
# STORE EMBEDDINGS
# ================================
def store_embeddings(
    chunks,
    filename="unknown"
):

    try:

        for chunk in chunks:

            chunk.metadata = clean_metadata(
                chunk.metadata
            )

            chunk.metadata["document_name"] = filename

        print(f"\nUploading {len(chunks)} chunks...")

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

        print("\nEmbeddings stored successfully")

    except Exception as e:

        print(f"\nEmbedding storage error: {e}")

        raise e


# ================================
# LOAD VECTOR DB
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