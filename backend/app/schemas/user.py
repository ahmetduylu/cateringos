from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    ad: str
    email: str
    password: str
    rol: str  # "marketing" veya "chief"


class UserOut(BaseModel):
    id: int
    ad: str
    email: str
    rol: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
