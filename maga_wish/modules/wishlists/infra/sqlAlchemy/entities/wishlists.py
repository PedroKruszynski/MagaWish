import uuid
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone

class WishlistBase(SQLModel):
    user_id: uuid.UUID = Field(foreign_key="users.id")
    product_id: uuid.UUID = Field(primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = None

class Wishlist(WishlistBase, table=True):
    __tablename__ = "wishlists"

    user: Optional["User"] = Relationship(back_populates="wishlists")
