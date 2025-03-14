from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request

from maga_wish.modules.users.dtos import CreateUserDTO
from maga_wish.modules.users.dtos.user import User
from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository
from maga_wish.modules.users.services import CreateUserService, GetUserByEmailService
from maga_wish.shared.infra.http.utils import SessionDep

router = APIRouter()


def getCreateUserService(
    userRepository: UserRepository = Depends(UserRepository), request: Request = None
) -> CreateUserService:
    redis_client = request.app.state.redis
    return CreateUserService(userRepository, redis_client)


def getUserByEmailService(
    userRepository: UserRepository = Depends(UserRepository), request: Request = None
) -> GetUserByEmailService:
    redis_client = request.app.state.redis
    return GetUserByEmailService(userRepository, redis_client)


@router.post("/", response_model=User)
async def create_user(
    *,
    session: SessionDep,
    user: CreateUserDTO,
    createUserService: CreateUserService = Depends(getCreateUserService),
    getUserByEmailService: GetUserByEmailService = Depends(getUserByEmailService),
) -> Any:
    """
    Create new user
    """
    userExist = await getUserByEmailService.getUser(session, user)

    if userExist:
        raise HTTPException(
            status_code=409,
            detail="E-mail unavailable",
        )

    response = await createUserService.create(session, user)

    return response
