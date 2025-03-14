from typing import Any, Annotated
from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from maga_wish.shared.environment.main import settings
from maga_wish.modules.authentication.dtos.token import Token
from maga_wish.modules.users.dtos import GetUserByEmailDTO
from maga_wish.modules.users.services import GetUserByEmailService
from maga_wish.shared.infra.http.utils import SessionDep
from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository
from maga_wish.modules.authentication.utils.verify_password import verify_password
from maga_wish.modules.authentication.utils.create_access_token import create_access_token


router = APIRouter()

def getUserByEmailService(
    userRepository: UserRepository = Depends(UserRepository),
    request: Request = None
) -> GetUserByEmailService:
    redis_client = request.app.state.redis
    return GetUserByEmailService(userRepository, redis_client)

@router.post("/login", response_model=Token)
async def access_token(
    session: SessionDep,
    formData: Annotated[OAuth2PasswordRequestForm, Depends()],
    getUserByEmailService: GetUserByEmailService = Depends(getUserByEmailService),
) -> Any:
    """
    Gen access token
    """
    userEmail = GetUserByEmailDTO(email=formData.username)
    user = await getUserByEmailService.getUser(session, userEmail)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="E-mail or password incorrect",
        )

    if not verify_password(formData.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="E-mail or password incorrect",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )