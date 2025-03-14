from uuid import UUID

from pydantic import BaseModel


class RestoreProductOfWishlistDTO(BaseModel):
    product_id: UUID
    user_id: UUID
