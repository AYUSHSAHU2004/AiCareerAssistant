from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db import crud
from app.models.resume import ResumeCreate, ResumeRead
from app.utils.file_handler import extract_text_from_pdf, extract_text_from_docx


router = APIRouter()

@router.post("/", response_model=ResumeRead)
def create_resume(resume_in: ResumeCreate, db: Session = Depends(get_db)):
    return crud.create_resume(db, resume_in)

@router.get("/user/{user_id}", response_model=List[ResumeRead])
def get_resumes_for_user(user_id: int, db: Session = Depends(get_db)):
    return crud.list_resumes_for_user(db, user_id)


@router.post("/upload", response_model=ResumeRead)
async def upload_resume_file(
    user_id: int = Form(...),
    title: str = Form("Uploaded Resume"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Validate extension
    filename = file.filename.lower()
    if not (filename.endswith(".pdf") or filename.endswith(".docx")):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX are supported")

    # Read file in-memory
    contents = await file.read()

    # Extract text depending on file type
    try:
        if filename.endswith(".pdf"):
            from io import BytesIO
            raw_text = extract_text_from_pdf(BytesIO(contents))
        else:  # .docx
            from io import BytesIO
            raw_text = extract_text_from_docx(BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {e}")

    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract any text from file")

    # Save in DB using existing CRUD
    resume_in = ResumeCreate(
        user_id=user_id,
        title=title if title else file.filename,
        raw_text=raw_text,
    )
    return crud.create_resume(db, resume_in)
