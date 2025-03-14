from uuid import UUID

from pydantic import BaseModel


class DeleteProductOfWishlistDTO(BaseModel):
    product_id: UUID
    user_id: UUID
