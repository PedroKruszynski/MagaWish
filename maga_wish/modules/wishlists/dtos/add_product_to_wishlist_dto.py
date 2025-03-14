from uuid import UUID

from pydantic import BaseModel


class AddProductToWishlistDTO(BaseModel):
    user_id: UUID
    product_id: UUID
