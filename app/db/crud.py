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



def create_job_source(db: Session, source_in: JobSourceCreate) -> models.JobSource:
    source = models.JobSource(
        url=str(source_in.url),
        label=source_in.label,
        user_id=source_in.user_id,
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return source

def list_job_sources(db: Session):
    sources = (
        db.query(models.JobSource)
        .order_by(models.JobSource.created_at.desc())
        .all()
    )

    return [
        JobSourceRead(
            id=s.id,
            url=s.base_url,   # ✅ mapped
            label=s.name,     # ✅ mapped
            user_id=None      # or s.user_id if exists
        )
        for s in sources
    ]