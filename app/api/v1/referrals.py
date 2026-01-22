from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.db.database import get_db
from app.services.referral_agent import send_top3_referral_emails_for_user

router = APIRouter(prefix="/referrals", tags=["referrals"])


@router.post("/user/{user_id}/send-top3")
def send_top3_referrals(user_id: int, db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    try:
        results = send_top3_referral_emails_for_user(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return results
