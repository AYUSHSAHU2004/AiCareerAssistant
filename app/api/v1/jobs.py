from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db import crud,models
from app.models.job_source import JobSourceCreate, JobSourceRead
from app.services.scraping_service import scrape_job_source_url


router = APIRouter()

# @router.post("/sources", response_model=JobSourceRead)
# def add_job_source(source_in: JobSourceCreate, db: Session = Depends(get_db)):
#     """
#     Add a new job source URL (e.g. a company's careers page).
#     """
#     return crud.create_job_source(db, source_in)

@router.get("/sources", response_model=List[JobSourceRead])
def get_job_sources(db: Session = Depends(get_db)):
    """
    List all stored job source URLs.
    """
    return crud.list_job_sources(db)

@router.post("/sources/{source_id}/scrape_test")
def scrape_job_source(
    source_id: int,
    db: Session = Depends(get_db),
):
    """
    Fetch the stored job source URL, load it via LangChain WebBaseLoader,
    and return some text snippets for inspection.
    """
    source = db.query(models.JobSource).get(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Job source not found")

    try:
        snippets = scrape_job_source_url(source.url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scrape failed: {e}")

    return {
        "source_id": source.id,
        "url": source.url,
        "snippet_count": len(snippets),
        "snippets": snippets,
    }

