from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.db.database import get_db
from app.db import models
from app.services.resume_embeddings import search_jobs_for_resume_text
from app.services.job_rerank import rerank_jobs_with_llm



router = APIRouter(prefix="/resumes", tags=["resume-match"])


@router.get("/user/{user_id}/matches", response_model=List[dict])
def match_jobs_for_user_resume(
    user_id: int,
    k: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    # 1) Load latest resume for this user
    resume = (
        db.query(models.Resume)  # use your actual Resume model name
        .filter(models.Resume.user_id == user_id)
        .order_by(models.Resume.id.desc())
        .first()
    )
    if not resume:
        raise HTTPException(status_code=404, detail="No resume found for user")

    raw_text = resume.raw_text
    if not raw_text or not raw_text.strip():
        raise HTTPException(status_code=400, detail="Resume has no extracted text")

    # 2) Search jobs using resume text
    docs = search_jobs_for_resume_text(raw_text, k=k)

    job_ids = [d.metadata["job_id"] for d in docs]
    if not job_ids:
        return []

    # 3) Fetch full job rows
    jobs = (
        db.query(models.Job)
        .filter(models.Job.id.in_(job_ids))
        .all()
    )
    job_by_id = {j.id: j for j in jobs}

    # 4) Map back in doc order
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
                "score_hint": d.page_content[:120],  # optional snippet
            }
        )
    return results


@router.get("/user/{user_id}/smart-matches")
def smart_match_jobs_for_user_resume(
    user_id: int,
    initial_k: int = Query(30, ge=5, le=100),  # how many from FAISS
    top_n: int = Query(10, ge=1, le=30),       # how many after LLM rerank
    db: Session = Depends(get_db),
):
    # 1) Latest resume
    resume = (
        db.query(models.Resume)
        .filter(models.Resume.user_id == user_id)
        .order_by(models.Resume.id.desc())
        .first()
    )
    if not resume:
        raise HTTPException(status_code=404, detail="No resume found for user")

    raw_text = resume.raw_text
    if not raw_text or not raw_text.strip():
        raise HTTPException(status_code=400, detail="Resume has no extracted text")

    # 2) Initial candidates from FAISS
    docs = search_jobs_for_resume_text(raw_text, k=initial_k)
    if not docs:
        return []

    # 3) LLM rerank
    scored = rerank_jobs_with_llm(raw_text, docs, top_n=top_n)
    if not scored:
        return []

    # 4) Fetch jobs by id
    job_ids = [s["job_id"] for s in scored if s["job_id"] is not None]
    if not job_ids:
        return []

    jobs = (
        db.query(models.Job)
        .filter(models.Job.id.in_(job_ids))
        .all()
    )
    job_by_id = {j.id: j for j in jobs}

    results: List[Dict[str, Any]] = []
    for s in scored:
        job = job_by_id.get(s["job_id"])
        if not job:
            continue
        results.append(
            {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "link": getattr(job, "link", None),
                "score": s["score"],
                "reason": s["reason"],
            }
        )

    return results

