from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any

from app.db.database import get_db
from app.db import models

router = APIRouter(prefix="/admin/jobs", tags=["jobs-admin"])


class JobSourceCreate(BaseModel):
    name: str
    base_url: str
    scraper_type: str = "amazon_dom"
    config_json: Dict[str, Any] = {}
    refresh_interval_hours: int = 24
    enabled: bool = True


@router.post("/sources", response_model=dict)
def create_job_source(payload: JobSourceCreate, db: Session = Depends(get_db)):
    source = models.JobSource(
        name=payload.name,
        base_url=payload.base_url,
        scraper_type=payload.scraper_type,
        config_json=payload.config_json,
        refresh_interval_hours=payload.refresh_interval_hours,
        enabled=payload.enabled,
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return {"id": source.id, "name": source.name}


