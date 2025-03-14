from uuid import UUID

from pydantic import BaseModel


class GetUserByIdDTO(BaseModel):
    id: UUID
