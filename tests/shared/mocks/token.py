from datetime import timedelta

from maga_wish.modules.authentication.dtos.token import Token
from maga_wish.modules.authentication.utils.create_access_token import (
    create_access_token,
)

from .user import user

token = Token(access_token=create_access_token(user.id, expires_delta=timedelta(10000)))

bearerToken = {"Authorization": f"Bearer {token.access_token}"}
