from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models

router = APIRouter(prefix="/referral-targets", tags=["referral-targets"])


@router.post("/")
def create_referral_target(
    company_name: str,
    employee_name: str,
    employee_email: str,
    db: Session = Depends(get_db),
):
    target = models.EmployeeReferralTarget(
        company_name=company_name,
        employee_name=employee_name,
        employee_email=employee_email,
    )

    db.add(target)
    db.commit()
    db.refresh(target)

    return {
        "message": "Referral target added",
        "data": {
            "id": target.id,
            "company": target.company_name,
            "employee": target.employee_name,
            "email": target.employee_email,
        },
    }