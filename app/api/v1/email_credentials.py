from app.db.crud_email_credential import (
    create_or_update_email_credential,
    get_email_credential_by_user_id,
)
from app.db.database import get_db
from app.models.email_credential import (
    EmailCredentialCreate,
    EmailCredentialRead,
)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=EmailCredentialRead)
def save_email_credential(
    credential: EmailCredentialCreate,
    db: Session = Depends(get_db),
):
    return create_or_update_email_credential(db, credential)


@router.get("/user/{user_id}", response_model=EmailCredentialRead)
def get_email_credential(
    user_id: int,
    db: Session = Depends(get_db),
):
    credential = get_email_credential_by_user_id(db, user_id)

    if credential is None:
        raise HTTPException(
            status_code=404,
            detail="Email credential not found",
        )

    return credential
