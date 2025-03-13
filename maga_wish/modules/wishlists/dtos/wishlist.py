from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class Wishlist(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    created_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
