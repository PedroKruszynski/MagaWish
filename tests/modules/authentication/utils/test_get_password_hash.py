from passlib.context import CryptContext

from maga_wish.modules.authentication.utils.get_password_hash import get_password_hash

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def test_get_password_hash():
    password = "mysecretpassword"
    hashed_password = get_password_hash(password)

    assert pwd_context.verify(password, hashed_password) is True
    assert pwd_context.verify("wrongpassword", hashed_password) is False
