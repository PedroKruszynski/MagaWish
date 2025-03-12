from typing import Any
from fastapi import APIRouter, Depends, Request, HTTPException
from uuid import UUID

from maga_wish.modules.users.dtos import GetUserByIdDTO
from maga_wish.modules.users.dtos.user import User
from maga_wish.modules.users.services import GetUserByIdService
from maga_wish.shared.infra.http.utils import SessionDep
from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository


router = APIRouter()

def getUserByIdService(
    userRepository: UserRepository = Depends(UserRepository),
    request: Request = None
) -> GetUserByIdService:
    redis_client = request.app.state.redis
    return GetUserByIdService(userRepository, redis_client)

@router.get("/{user_id}", response_model=User)
async def get_user_by_id(
    session: SessionDep,
    user_id: UUID,
    getUsersService: GetUserByIdService = Depends(getUserByIdService),
) -> Any:
    """
    Get a specific user by id
    """
    data = GetUserByIdDTO(id=user_id)
    user = await getUsersService.getUserById(session, data)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    
    return user