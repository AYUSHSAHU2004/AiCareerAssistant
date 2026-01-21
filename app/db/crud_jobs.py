# app/db/crud_jobs.py
from typing import List
from sqlalchemy.orm import Session
from app.db import models
from app.services.job_schema import JobDict


def upsert_jobs_for_source(
    db: Session,
    source: models.JobSource,
    jobs: List[JobDict],
) -> None:
    """
    Insert/update jobs for a given source.
    """
    for job_data in jobs:
        existing = (
            db.query(models.Job)
            .filter(
                models.Job.source_id == source.id,
                models.Job.external_job_id == job_data["external_job_id"],
            )
            .first()
        )

        if existing:
            existing.title = job_data["title"]
            existing.company = job_data.get("company")
            existing.location = job_data.get("location")
            existing.link = job_data["link"]
            existing.posted_date = job_data.get("posted_date")
            existing.description = job_data.get("description")
            existing.raw_data = job_data["raw_data"]
            existing.is_active = True
        else:
            new_job = models.Job(
                source_id=job_data["source_id"],
                external_job_id=job_data["external_job_id"],
                title=job_data["title"],
                company=job_data.get("company"),
                location=job_data.get("location"),
                link=job_data["link"],
                posted_date=job_data.get("posted_date"),
                description=job_data.get("description"),
                raw_data=job_data["raw_data"],
            )
            db.add(new_job)

    db.commit()
