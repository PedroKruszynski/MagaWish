from uuid import UUID

from pydantic import BaseModel, EmailStr


class DeleteUserDTO(BaseModel):
    id: UUID
    email: EmailStr | None = None
