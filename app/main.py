from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1 import users

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(users.router, prefix="/api/v1/users", tags=["users"])





@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.APP_NAME}
