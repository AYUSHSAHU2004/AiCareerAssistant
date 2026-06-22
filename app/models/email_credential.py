from datetime import datetime

from pydantic import BaseModel, EmailStr


class EmailCredentialCreate(BaseModel):
    user_id: int
    email: EmailStr
    app_password: str


class EmailCredentialRead(BaseModel):
    id: int
    user_id: int
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
