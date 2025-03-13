from pydantic import BaseModel
from uuid import UUID

class AddProductToWishlistDTO(BaseModel):
    user_id: UUID
    product_id: UUID
