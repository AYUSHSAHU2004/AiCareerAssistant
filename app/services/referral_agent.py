from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.db import models
from app.services.resume_embeddings import search_jobs_for_resume_text
from app.services.referral_email_agent import (
    generate_referral_email,
    extract_subject_body,
)

def find_employee_for_company(
    db: Session, company_name: str
) -> models.EmployeeReferralTarget | None:
    return (
        db.query(models.EmployeeReferralTarget)
        .filter(models.EmployeeReferralTarget.company_name == company_name)
        .first()
    )
