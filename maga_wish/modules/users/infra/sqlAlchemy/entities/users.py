from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import ConfigDict, EmailStr
from sqlmodel import Field, Relationship, SQLModel

from maga_wish.modules.wishlists.infra.sqlAlchemy.entities.wishlists import Wishlist


class UserBase(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    hashed_password: str


class User(UserBase, table=True):
    __tablename__ = "users"

    wishlists: list["Wishlist"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    model_config = ConfigDict(from_attributes=True)
