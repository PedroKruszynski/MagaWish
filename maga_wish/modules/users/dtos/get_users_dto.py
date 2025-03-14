from fastapi import Query
from pydantic import BaseModel


class GetUsersDTO(BaseModel):
    limit: int = Query(10, gt=0)
    page: int = Query(1, gt=0)
