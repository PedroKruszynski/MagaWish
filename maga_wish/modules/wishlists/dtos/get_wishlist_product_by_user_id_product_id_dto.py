from pydantic import BaseModel
from pydantic import BaseModel
from uuid import UUID

class GetWishlistProductByUserIdProductIdDTO(BaseModel):
    product_id: UUID
    user_id: UUID