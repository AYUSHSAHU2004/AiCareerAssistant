from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey,Boolean,JSON,UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    resumes = relationship("Resume", back_populates="user")
