from uuid import UUID

from pydantic import BaseModel


class DeleteUserDTO(BaseModel):
    id: UUID
