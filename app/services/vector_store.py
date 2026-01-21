from typing import List, Optional
import os

from sqlalchemy.orm import Session
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.db import models

# Directory where the FAISS index will be stored (folder, not single file)
_INDEX_DIR = "job_faiss_index"

# Embedding model
_embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": False},
)

# In-memory cache of the loaded store
_STORE: Optional[FAISS] = None




def rebuild_vector_store(db: Session) -> None:
    """
    Rebuild the FAISS index from all active jobs in the database.
    Saves the index in the _INDEX_DIR directory.
    """
    os.makedirs(_INDEX_DIR, exist_ok=True)

    # Load all active jobs from DB
    jobs = db.query(models.Job).filter(models.Job.is_active == True).all()

    texts: List[str] = []
    metadatas: List[dict] = []

    for job in jobs:
        content = job.description or ""
        if not content.strip():
            continue

        texts.append(content)
        metadatas.append(
            {
                "job_id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
            }
        )

    if not texts:
        print("No jobs to index.")
        return

    # Build FAISS index in memory
    store = FAISS.from_texts(
        texts=texts,
        embedding=_embeddings,
        metadatas=metadatas,
    )

    # Save to directory; this will create/overwrite the folder contents
    store.save_local(_INDEX_DIR)
    print(f"Indexed {len(texts)} jobs into directory '{_INDEX_DIR}'")



