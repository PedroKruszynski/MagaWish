from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from uuid import UUID

class UpdateUserDTO(BaseModel):
    id: Optional[UUID] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None

    @field_validator('id', mode='before')
    def ignore_id(cls, v):
        return None

    class Config:
        fields = {'id': {'exclude': True}}

