from uuid import UUID, uuid4
from typing import List, Optional
from datetime import datetime, timezone
from pydantic import EmailStr, ConfigDict
from sqlmodel import Field, SQLModel, Relationship

from maga_wish.modules.wishlists.infra.sqlAlchemy.entities.wishlists import Wishlist

class UserBase(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    hashed_password: str

class User(UserBase, table=True):
    __tablename__ = "users"
    
    wishlists: List["Wishlist"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

    model_config = ConfigDict(from_attributes=True)