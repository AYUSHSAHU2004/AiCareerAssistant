import os

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def build_vector_store(docs, save_path: str):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Existing context -> append documents
    if os.path.exists(save_path):
        vector_store = FAISS.load_local(
            save_path,
            embeddings,
            allow_dangerous_deserialization=True,
        )

        vector_store.add_documents(docs)

    # New context -> create fresh FAISS
    else:
        vector_store = FAISS.from_documents(
            docs,
            embeddings,
        )

    # Save updated index
    vector_store.save_local(save_path)

    return vector_store
