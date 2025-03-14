from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Wishlist(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    created_at: datetime
    deleted_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
