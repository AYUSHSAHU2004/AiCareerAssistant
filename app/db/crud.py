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

