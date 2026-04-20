from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import os

from app.services.load_youtube_documents import load_youtube_documents
from app.services.load_wikipedia_documents import load_wikipedia_documents
from app.services.load_pdf_documents import load_pdf_documents
from app.services.build_vector_store import build_vector_store

router = APIRouter()

@router.post("/upload")
async def upload_context(
    user_id: int = Form(...),
    context_id: str = Form(...),   # ✅ user provides this
    youtube_url: Optional[str] = Form(None),
    wiki_query: Optional[str] = Form(None),
    pdf: Optional[UploadFile] = File(None),
):
    # validate context_id
    if not context_id.replace("_", "").replace("-", "").isalnum():
        raise HTTPException(status_code=400, detail="Invalid context_id")

    all_docs = []

    if youtube_url:
        all_docs.extend(load_youtube_documents(youtube_url))

    if wiki_query:
        all_docs.extend(load_wikipedia_documents(wiki_query))

    if pdf:
        all_docs.extend(load_pdf_documents(pdf))

    if not all_docs:
        raise HTTPException(status_code=400, detail="Provide at least one source")

    faiss_path = f"vectorstore/{user_id}/{context_id}"

    # prevent overwrite
    if os.path.exists(faiss_path):
        raise HTTPException(status_code=400, detail="Context already exists")

    # build + save FAISS
    build_vector_store(all_docs, save_path=faiss_path)

    return {
        "context_id": context_id,
        "faiss_path": faiss_path,
        "context":all_docs 
    }