from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class DeleteUserDTO(BaseModel):
    id: UUID
    email: Optional[EmailStr] = None

