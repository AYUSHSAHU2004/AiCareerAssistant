import os
from langchain_community.vectorstores import FAISS

# Define a persistent directory for your vector store
DB_FAISS_PATH = 'vectorstore/db_faiss'

def build_vector_store(docs):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Check if the local index already exists
    if os.path.exists(DB_FAISS_PATH):
        print(f"[VectorStore] Index found at {DB_FAISS_PATH}. Loading...")
        # Load the existing index from disk
        # allow_dangerous_deserialization is required for loading FAISS files
        vector_store = FAISS.load_local(
            DB_FAISS_PATH, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
    else:
        print("[VectorStore] No index found. Creating new index...")
        # Create the index from documents
        vector_store = FAISS.from_documents(docs, embeddings)
        
        # Save the index to disk for next time
        vector_store.save_local(DB_FAISS_PATH)
        print(f"[VectorStore] ✅ Index created and saved to {DB_FAISS_PATH}")

    return vector_store