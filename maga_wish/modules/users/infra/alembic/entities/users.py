import uuid
from typing import List, Optional
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship


class UserBase(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    is_superuser: bool = False
    hashed_password: str

class User(UserBase, table=True):
    __tablename__ = "users"
    
    wishlist: List["Product"] = Relationship(back_populates="wishlisted_by", sa_relationship_kwargs={"cascade": "all, delete-orphan"})