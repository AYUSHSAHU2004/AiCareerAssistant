# app/services/job_schema.py
from typing import TypedDict, Optional
from datetime import datetime


class JobDict(TypedDict):
    source_id: int
    external_job_id: str

    title: str
    company: Optional[str]
    location: Optional[str]
    link: str
    posted_date: Optional[datetime]
    description: Optional[str]

    raw_data: dict
