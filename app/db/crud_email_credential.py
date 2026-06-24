from app.db import models
from app.models.email_credential import EmailCredentialCreate
from app.utils.crypto import encrypt
from sqlalchemy.orm import Session


def create_or_update_email_credential(
    db: Session,
    credential: EmailCredentialCreate,
):
    existing = (
        db.query(models.UserEmailCredential)
        .filter(models.UserEmailCredential.user_id == credential.user_id)
        .first()
    )

    if existing:
        existing.email = credential.email
        existing.encrypted_app_password = encrypt(credential.app_password)

        db.commit()
        db.refresh(existing)
        return existing

    new_credential = models.UserEmailCredential(
        user_id=credential.user_id,
        email=credential.email,
        encrypted_app_password=encrypt(credential.app_password),
    )

    db.add(new_credential)
    db.commit()
    db.refresh(new_credential)

    return new_credential


def get_email_credential_by_user_id(
    db: Session,
    user_id: int,
):
    return (
        db.query(models.UserEmailCredential)
        .filter(models.UserEmailCredential.user_id == user_id)
        .first()
    )
