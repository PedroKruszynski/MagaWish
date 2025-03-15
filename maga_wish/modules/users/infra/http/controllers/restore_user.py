from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request

from maga_wish.modules.users.dtos import GetUserByIdDTO, RestoreUserDTO
from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository
from maga_wish.modules.users.services import GetUserByIdService, RestoreUserService
from maga_wish.shared.infra.http.utils import (
    CurrentUserDep,
    MessageToReturn,
    SessionDep,
)

router = APIRouter()


def restoreUserService(
    userRepository: UserRepository = Depends(UserRepository), request: Request = None
) -> RestoreUserService:
    redis_client = request.app.state.redis
    return RestoreUserService(userRepository, redis_client)


def getUserByIdService(
    userRepository: UserRepository = Depends(UserRepository), request: Request = None
) -> GetUserByIdService:
    redis_client = request.app.state.redis
    return GetUserByIdService(userRepository, redis_client)


@router.put("/{user_id}", response_model=MessageToReturn)
async def restore_user(
    *,
    session: SessionDep,
    _: CurrentUserDep,
    user_id: UUID,
    restoreUserService: RestoreUserService = Depends(restoreUserService),
    getUserByIdService: GetUserByIdService = Depends(getUserByIdService),
) -> Any:
    """
    Restore a user
    """
    data = GetUserByIdDTO(id=user_id)
    user = await getUserByIdService.getUserById(session, data)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if not user.deleted_at:
        raise HTTPException(
            status_code=400,
            detail="User not deleted",
        )

    data = RestoreUserDTO(id=user_id)
    userRestored = await restoreUserService.restoreUser(session, data)

    if not userRestored:
        raise HTTPException(
            status_code=400,
            detail="User not restored",
        )

    return MessageToReturn(success=True, data=userRestored, message="User Restored")
