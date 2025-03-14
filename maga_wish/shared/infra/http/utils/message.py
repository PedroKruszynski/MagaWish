from sqlmodel import SQLModel


class MessageToReturn(SQLModel):
    success: bool
    message: str
