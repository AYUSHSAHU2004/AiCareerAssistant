# app/services/resume_embeddings.py
from app.services.vector_store import load_vector_store, _embeddings  # reuse same model

def search_jobs_for_resume_text(raw_text: str, k: int = 10):
    """
    Take resume raw_text, embed it, and return top-k matching job docs.
    """
    store = load_vector_store()
    # # similarity_search_by_vector expects an embedding vector
    # query_vec = _embeddings.embed_query(raw_text)
    # docs = store.similarity_search_by_vector(query_vec, k=k)

    retriever = store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )

    # 3. Invoke the retriever
    # You pass RAW TEXT now, not the vector. The retriever handles the embedding.
    docs = retriever.invoke(raw_text)
    return docs
