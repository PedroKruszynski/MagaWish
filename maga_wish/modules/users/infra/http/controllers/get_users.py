from typing import Any, List
from fastapi import APIRouter, Depends, Query

from maga_wish.modules.users.dtos.user import User
from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository
from maga_wish.modules.users.services import GetUsersService
from maga_wish.modules.users.dtos import GetUsersDTO
from maga_wish.shared.infra.http.utils import (
    CurrentUserDep,
    SessionDep
)

router = APIRouter()

def getUsersService(
    userRepository: UserRepository = Depends(UserRepository),
) -> GetUsersService:
    return GetUsersService(userRepository)

def getUsersDto(
    limit: int = Query(10, gt=0), 
    page: int = Query(1, gt=0)
) -> GetUsersDTO:
    return GetUsersDTO(limit=limit, page=page)

@router.get("/", response_model=List[User])
async def get_users(
    *,
    session: SessionDep,
    _: CurrentUserDep,
    data: GetUsersDTO = Depends(getUsersDto),
    getUsersService: GetUsersService = Depends(getUsersService),
) -> Any:
    """
    Get all users
    """
    users = await getUsersService.getUsers(session, data)
    return users