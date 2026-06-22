from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import (
    email_credentials,
    jobs,
    jobs_admin,
    jobs_search,
    rag,
    referral_targets,
    referrals,
    resume_match,
    resumes,
    upload,
    users,
)
from app.config import settings

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(resumes.router, prefix="/api/v1/resumes", tags=["resumes"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["jobs"])
app.include_router(jobs_admin.router, prefix="/api/v1")
app.include_router(jobs_search.router, prefix="/api/v1")
app.include_router(resume_match.router, prefix="/api/v1")
app.include_router(referrals.router, prefix="/api/v1")
app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(rag.router, prefix="/api/v1/rag", tags=["rag"])
app.include_router(referral_targets.router)
app.include_router(
    email_credentials.router,
    prefix="/api/v1/email-credentials",
    tags=["Email Credentials"],
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.APP_NAME}
