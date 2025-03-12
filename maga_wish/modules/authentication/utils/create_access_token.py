from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from maga_wish.shared.environment.main import settings
from maga_wish.modules.authentication.utils.algorithm import algorithm

def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=algorithm())
    return encoded_jwt