from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class WishlistBase(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    product_id: UUID = Field(primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: datetime | None = None


class Wishlist(WishlistBase, table=True):
    __tablename__ = "wishlists"

    user: Optional["User"] = Relationship(back_populates="wishlists")  # noqa: F821
