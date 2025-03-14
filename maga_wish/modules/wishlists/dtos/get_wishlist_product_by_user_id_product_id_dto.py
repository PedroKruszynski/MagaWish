from uuid import UUID

from pydantic import BaseModel


class GetWishlistProductByUserIdProductIdDTO(BaseModel):
    product_id: UUID
    user_id: UUID
