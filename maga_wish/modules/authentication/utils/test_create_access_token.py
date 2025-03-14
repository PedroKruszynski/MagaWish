from datetime import datetime, timedelta, timezone

import jwt
import pytest

from maga_wish.modules.authentication.utils.algorithm import algorithm
from maga_wish.modules.authentication.utils.create_access_token import (
    create_access_token,
)
from maga_wish.shared.environment.main import settings


def test_create_access_token():
    subject = "testuser"
    expires_delta = timedelta(minutes=15)
    token = create_access_token(subject, expires_delta)

    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[algorithm()])

    assert decoded_token["sub"] == subject
    assert "exp" in decoded_token
    assert datetime.fromtimestamp(decoded_token["exp"], timezone.utc) > datetime.now(
        timezone.utc
    )


def test_create_access_token_expired():
    subject = "testuser"
    expires_delta = timedelta(seconds=-1)
    token = create_access_token(subject, expires_delta)

    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(token, settings.SECRET_KEY, algorithms=[algorithm()])
