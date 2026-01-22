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

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    raw_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resumes")

class JobSource(Base):
    __tablename__ = "job_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    base_url = Column(Text, nullable=False)
    scraper_type = Column(Text, nullable=False)
    config_json = Column(JSON, nullable=False, default={})

    refresh_interval_hours = Column(Integer, nullable=False, default=24)
    enabled = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    jobs = relationship("Job", back_populates="source")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    source_id = Column(Integer, ForeignKey("job_sources.id", ondelete="CASCADE"), nullable=False)
    external_job_id = Column(Text, nullable=False)

    title = Column(Text, nullable=False)
    company = Column(Text)
    location = Column(Text)
    link = Column(Text, nullable=False)
    posted_date = Column(DateTime(timezone=True))
    description = Column(Text)

    raw_data = Column(JSON, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    first_seen_at = Column(DateTime(timezone=True), server_default=func.now())
    last_seen_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    source = relationship("JobSource", back_populates="jobs")

    __table_args__ = (
        UniqueConstraint("source_id", "external_job_id", name="uq_jobs_source_ext_id"),
    )


class EmployeeReferralTarget(Base):
    """Stores employee contacts for referral requests."""
    __tablename__ = "employee_referral_targets"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False, index=True)
    employee_name = Column(String(255), nullable=False)
    employee_email = Column(String(255), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
