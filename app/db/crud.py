from sqlalchemy.orm import Session
from app.db import models
from app.models.user import UserCreate
from app.models.resume import ResumeCreate




def create_user(db: Session, user_in: UserCreate) -> models.User:
    user = models.User(email=user_in.email, name=user_in.name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()

def create_resume(db: Session, resume_in: ResumeCreate) -> models.Resume:
    resume = models.Resume(
        user_id=resume_in.user_id,
        title=resume_in.title,
        raw_text=resume_in.raw_text,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume

def list_resumes_for_user(db: Session, user_id: int):
    return db.query(models.Resume).filter(models.Resume.user_id == user_id).all()