from collections.abc import Generator
from typing import Annotated
from fastapi import Depends, HTTPException, status
from pydantic import ValidationError
from jwt.exceptions import InvalidTokenError
import jwt

from maga_wish.shared.environment.main import settings
from maga_wish.shared.infra.http.utils.session import SessionDep
from maga_wish.shared.infra.http.utils.oauth2 import TokenDep
from maga_wish.modules.authentication.dtos.token_payload import TokenPayload
from maga_wish.modules.authentication.utils.algorithm import algorithm
from maga_wish.modules.users.dtos.user import User
from maga_wish.modules.users.infra.sqlAlchemy.entities.users import UserBase

def getCurrentUser(token: TokenDep) -> None:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[algorithm()]
        )
        TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
CurrentUserDep = Annotated[User, Depends(getCurrentUser)]