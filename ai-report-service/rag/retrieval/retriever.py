from rag.embeddings.vector_store import load_vector_db


# ================================
# RETRIEVE DOCUMENTS
# ================================
def retrieve_docs(query, k=3):

    db = load_vector_db()

    results = db.similarity_search(
        query=query,
        k=k
    )

    return results
