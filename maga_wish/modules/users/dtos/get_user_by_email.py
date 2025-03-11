from pydantic import BaseModel, EmailStr

class GetUserByEmail(BaseModel):
    email: EmailStr
