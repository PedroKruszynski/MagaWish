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
from maga_wish.modules.authentication.utils import algorithm
from maga_wish.modules.users.dtos.user import User
from maga_wish.modules.users.infra.sqlAlchemy.entities.users import UserBase

def get_current_user(session: SessionDep, token: TokenDep) -> User:
    print(token)
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[algorithm]
        )
        tokenData = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    user = session.get(UserBase, tokenData.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return User.model_validate(user)

CurrentUser = Annotated[User, Depends(get_current_user)]