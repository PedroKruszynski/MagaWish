from pydantic import BaseModel
from uuid import UUID

class GetUserByIdDTO(BaseModel):
    id: UUID
