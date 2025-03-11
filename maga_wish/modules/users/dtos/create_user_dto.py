from pydantic import BaseModel, EmailStr

class CreateUserDTO(BaseModel):
    email: EmailStr
    name: str
    password: str
