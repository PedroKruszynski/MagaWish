from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from maga_wish.shared.environment.main import settings

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

TokenDep = Annotated[str, Depends(reusable_oauth2)]
