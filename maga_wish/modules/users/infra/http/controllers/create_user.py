from typing import Any
from fastapi import APIRouter, Depends, Request
from fastapi import HTTPException

from maga_wish.modules.users.dtos.create_user_dto import CreateUserDTO
from maga_wish.modules.users.dtos.user import User
from maga_wish.modules.users.services import CreateUserService
from maga_wish.modules.users.services import GetUserByEmailService
from maga_wish.shared.infra.http.utils import SessionDep
from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository


router = APIRouter()

def getCreateUserService(
    user_repository: UserRepository = Depends(UserRepository),
    request: Request = None
) -> CreateUserService:
    redis_client = request.app.state.redis
    return CreateUserService(user_repository, redis_client)

def getUserByEmailService(
    user_repository: UserRepository = Depends(UserRepository),
    request: Request = None
) -> GetUserByEmailService:
    redis_client = request.app.state.redis
    return GetUserByEmailService(user_repository, redis_client)

@router.post("/", response_model=User)
async def get_user_by_id(
    *,
    request: Request,
    session: SessionDep,
    user: CreateUserDTO,
    create_user_service: CreateUserService = Depends(getCreateUserService),
    get_user_by_email: GetUserByEmailService = Depends(getUserByEmailService)
) -> Any:
    """
    Create new user
    """
    userExist = await get_user_by_email.getUser(session, user)

    if userExist:
        raise HTTPException(
            status_code=404,
            detail="E-mail unavailable",
        )

    response = await create_user_service.create(session, user)

    return response
    # user = session.get(User, user_id)
    # if user == current_user:
    #     return user
    # if not current_user.is_superuser:
    #     raise HTTPException(
    #         status_code=403,
    #         detail="The user doesn't have enough privileges",
    #     )
    # return user