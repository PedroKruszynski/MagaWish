from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request

from maga_wish.modules.users.dtos import (
    GetUserByEmailDTO,
    GetUserByIdDTO,
    UpdateUserDTO,
)
from maga_wish.modules.users.dtos.user import User
from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository
from maga_wish.modules.users.services import (
    GetUserByEmailService,
    GetUserByIdService,
    UpdateUserService,
)
from maga_wish.shared.infra.http.utils import CurrentUserDep, SessionDep

router = APIRouter()


def updateUserService(
    userRepository: UserRepository = Depends(UserRepository), request: Request = None
) -> UpdateUserService:
    redis_client = request.app.state.redis
    return UpdateUserService(userRepository, redis_client)


def getUserByEmailService(
    userRepository: UserRepository = Depends(UserRepository), request: Request = None
) -> GetUserByEmailService:
    redis_client = request.app.state.redis
    return GetUserByEmailService(userRepository, redis_client)


def getUserByIdService(
    userRepository: UserRepository = Depends(UserRepository), request: Request = None
) -> GetUserByIdService:
    redis_client = request.app.state.redis
    return GetUserByIdService(userRepository, redis_client)


@router.patch("/{user_id}", response_model=User)
async def update_user(
    *,
    session: SessionDep,
    _: CurrentUserDep,
    userData: UpdateUserDTO,
    user_id: UUID,
    updateUserService: UpdateUserService = Depends(updateUserService),
    getUserByIdService: GetUserByIdService = Depends(getUserByIdService),
    getUserByEmailService: GetUserByEmailService = Depends(getUserByEmailService),
) -> Any:
    """
    Update a user
    """
    if not any([userData.email, userData.name, userData.password]):
        raise HTTPException(
            status_code=400,
            detail="No data provided to update the user",
        )

    dataById = GetUserByIdDTO(id=user_id)
    userExist = await getUserByIdService.getUserById(session, dataById)

    if not userExist:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    if userData.email:
        dataByEmail = GetUserByEmailDTO(email=userData.email)
        userWithNewEmailExist = await getUserByEmailService.getUser(
            session, dataByEmail
        )

        if userWithNewEmailExist:
            raise HTTPException(
                status_code=409,
                detail="E-mail unavailable",
            )

    userData.id = user_id
    userUpdated = await updateUserService.update(session, userData)

    if not userUpdated:
        raise HTTPException(
            status_code=500,
            detail="Server Error",
        )

    return userUpdated
