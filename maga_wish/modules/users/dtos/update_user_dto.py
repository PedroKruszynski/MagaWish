from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator, model_validator


class UpdateUserDTO(BaseModel):
    id: UUID | None = None
    email: EmailStr | None = None
    name: str | None = None
    password: str | None = None

    @field_validator("id", mode="before")
    def ignore_id(cls, v):
        return None

    @model_validator(mode="before")
    def exclude_id(cls, values):
        values.pop("id", None)
        return values
