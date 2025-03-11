import uuid
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

class WishlistBase(SQLModel):
    __tablename__ = 'wishlists'

    user_id: uuid.UUID = Field(foreign_key="users.id")
    product_id: uuid.UUID = Field(primary_key=True)
    added_at: Optional[str] = Field(default=None)

class Wishlist(WishlistBase, table=True):
    __tablename__ = "Wishlist"

    user: Optional["User"] = Relationship(back_populates="wishlists")
