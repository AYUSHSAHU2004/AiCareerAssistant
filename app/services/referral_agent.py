from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.db import models
from app.services.resume_embeddings import search_jobs_for_resume_text
from app.services.referral_email_agent import (
    generate_referral_email,
    extract_subject_body,
)
from app.services.email_sender import queue_email


def find_employee_for_company(
    db: Session, company_name: str
) -> models.EmployeeReferralTarget | None:
    return (
        db.query(models.EmployeeReferralTarget)
        .filter(models.EmployeeReferralTarget.company_name == company_name)
        .first()
    )


def send_top3_referral_emails_for_user(
    db: Session, user_id: int
) -> List[Dict[str, Any]]:
    # 1) latest resume
    resume = (
        db.query(models.Resume)
        .filter(models.Resume.user_id == user_id)
        .order_by(models.Resume.id.desc())
        .first()
    )
    if not resume or not resume.raw_text:
        raise ValueError("No resume text found for user")

    raw_text = resume.raw_text

    # 2) top 3 related jobs from vector store
    docs = search_jobs_for_resume_text(raw_text, k=3)
    if not docs:
        return []

    results: List[Dict[str, Any]] = []

    for d in docs:
        company_name = d.metadata.get("company", "")
        job_title = d.metadata.get("title", "")
        job_description = d.page_content
        job_id = d.metadata.get("job_id")

        # 3) find employee email for this company
        employee = find_employee_for_company(db, company_name)
        if not employee:
            results.append(
                {
                    "job_id": job_id,
                    "company": company_name,
                    "status": "no_employee_for_company",
                }
            )
            continue

        # 4) generate email text with LLM
        email_text = generate_referral_email(
            candidate_resume=raw_text,
            job_title=job_title,
            job_description=job_description,
            employee_name=employee.employee_name,
            company_name=company_name,
        )

        subject, body = extract_subject_body(email_text)

        # 5) queue email via your Node /api/email
        api_response = queue_email(
            to=employee.employee_email,
            subject=subject,
            text=body,
        )

        results.append(
            {
                "job_id": job_id,
                "company": company_name,
                "employee_email": employee.employee_email,
                "status": "queued",
                "email_api_response": api_response,
            }
        )

    return results
