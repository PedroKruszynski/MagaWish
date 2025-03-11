from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
