from uuid import UUID

from pydantic import BaseModel


class RestoreUserDTO(BaseModel):
    id: UUID
