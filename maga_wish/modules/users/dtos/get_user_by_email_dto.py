from pydantic import BaseModel, EmailStr


class GetUserByEmailDTO(BaseModel):
    email: EmailStr
