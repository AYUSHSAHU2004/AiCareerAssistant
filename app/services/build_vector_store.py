import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

def build_vector_store(docs, save_path: str):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # create FAISS
    vector_store = FAISS.from_documents(docs, embeddings)

    # ensure directory exists
    os.makedirs(save_path, exist_ok=True)

    # save
    vector_store.save_local(save_path)

    return vector_store