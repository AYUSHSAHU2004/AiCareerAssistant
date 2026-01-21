from pydantic import BaseModel, AnyHttpUrl
from typing import Optional

class JobSourceCreate(BaseModel):
    url: AnyHttpUrl
    label: Optional[str] = None
    user_id: Optional[int] = None  # who added it; can be null for now

class JobSourceRead(BaseModel):
    id: int
    url: AnyHttpUrl
    label: Optional[str] = None
    user_id: Optional[int] = None

    class Config:
        from_attributes = True
