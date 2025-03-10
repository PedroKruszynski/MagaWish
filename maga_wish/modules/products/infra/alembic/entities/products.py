import uuid
from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship


class ProductBase(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(index=True, max_length=255)
    price: float = Field(gt=0)
    image: Optional[str] = Field(default=None, max_length=500)
    brand: Optional[str] = Field(default=None, max_length=255)
    reviewScore: Optional[float] = Field(default=None, ge=0, le=5)

class Product(ProductBase, table=True):
    __tablename__ = "products"
    
    wishlisted_by: List["User"] = Relationship(back_populates="wishlists")