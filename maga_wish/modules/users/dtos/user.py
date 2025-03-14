from pydantic import BaseModel, EmailStr, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)
