from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request

from maga_wish.modules.users.dtos import GetUserByIdDTO
from maga_wish.modules.users.dtos.user import User
from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository
from maga_wish.modules.users.services import GetUserByIdService
from maga_wish.shared.infra.http.utils import CurrentUserDep, SessionDep

router = APIRouter()


def getUserByIdService(
    userRepository: UserRepository = Depends(UserRepository), request: Request = None
) -> GetUserByIdService:
    redis_client = request.app.state.redis
    return GetUserByIdService(userRepository, redis_client)


@router.get("/{user_id}", response_model=User)
async def get_user_by_id(
    session: SessionDep,
    _: CurrentUserDep,
    user_id: UUID,
    getUserByIdService: GetUserByIdService = Depends(getUserByIdService),
) -> Any:
    """
    Get a specific user by id
    """
    data = GetUserByIdDTO(id=user_id)
    user = await getUserByIdService.getUserById(session, data)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user
