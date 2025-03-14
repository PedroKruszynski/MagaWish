from typing import Any

from sqlmodel import SQLModel


class MessageToReturn(SQLModel):
    success: bool
    data: Any | None = None
    message: str
