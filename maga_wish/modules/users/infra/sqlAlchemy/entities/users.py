import uuid
from uuid import UUID
from typing import List, Optional
from datetime import datetime, timezone
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship

from maga_wish.modules.whislists.infra.alembic.entities.whislists import Wishlist

class UserBase(SQLModel):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    hashed_password: str

class User(UserBase, table=True):
    __tablename__ = "users"
    
    wishlists: List["Wishlist"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

    class Config:
        from_attributes = True