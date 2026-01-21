from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db import models
from app.services.vector_store import load_vector_store

router = APIRouter(prefix="/jobs", tags=["jobs-search"])


@router.get("/search", response_model=List[dict])
def search_jobs(
    q: str = Query(..., description="Search text, e.g. 'SDE backend Bangalore'"),
    k: int = 10,
    db: Session = Depends(get_db),
):
    store = load_vector_store()
    docs = store.similarity_search(q, k=k)  # returns List[Document] [web:194][web:200]

    job_ids = [d.metadata["job_id"] for d in docs]
    if not job_ids:
        return []

    jobs = (
        db.query(models.Job)
        .filter(models.Job.id.in_(job_ids))
        .all()
    )

    # Map Job -> response, preserving doc order
    job_by_id = {j.id: j for j in jobs}
    results = []
    for d in docs:
        job = job_by_id.get(d.metadata["job_id"])
        if not job:
            continue
        results.append(
            {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "link": job.link,
                "source_id": job.source_id,
            }
        )
    return results
