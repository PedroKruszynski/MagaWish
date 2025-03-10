import uuid
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

class WishlistBase(SQLModel, table=True):
    __tablename__ = 'wishlists'

    user_id: uuid.UUID = Field(foreign_key="user.id", primary_key=True)
    product_id: uuid.UUID = Field(foreign_key="product.id", primary_key=True)
    added_at: Optional[str] = Field(default=None)

    user: "User" = Relationship(back_populates="wishlists", sa_relationship_kwargs={"lazy": "joined"})
    product: "Product" = Relationship(back_populates="wishlisted_by", sa_relationship_kwargs={"lazy": "joined"})
