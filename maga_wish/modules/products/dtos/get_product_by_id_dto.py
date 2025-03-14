from pydantic import BaseModel
from uuid import UUID

class GetProductByIdDTO(BaseModel):
    id: UUID