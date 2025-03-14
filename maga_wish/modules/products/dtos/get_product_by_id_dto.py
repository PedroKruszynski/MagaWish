from uuid import UUID

from pydantic import BaseModel


class GetProductByIdDTO(BaseModel):
    id: UUID
