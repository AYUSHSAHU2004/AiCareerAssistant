from pydantic import BaseModel
from typing import List

class ResumeCreate(BaseModel):
    user_id: int
    title: str
    raw_text: str

class ResumeRead(BaseModel):
    id: int
    user_id: int
    title: str
    raw_text: str

    class Config:
        from_attributes = True
