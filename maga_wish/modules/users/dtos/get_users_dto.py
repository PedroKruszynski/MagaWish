from pydantic import BaseModel
from fastapi import Query

class GetUsersDTO(BaseModel):
    limit: int = Query(10, gt=0)
    page: int = Query(1, gt=0)
