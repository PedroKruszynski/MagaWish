from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, field_validator, model_validator


class GetWishlistByUserIdDTO(BaseModel):
    user_id: UUID | None = None
    limit: int = Query(10, gt=0)
    page: int = Query(1, gt=0)

    @field_validator("user_id", mode="before")
    def ignore_user_id(cls, v):
        return None

    @model_validator(mode="before")
    def exclude_user_id(cls, values):
        values.pop("user_id", None)
        return values
