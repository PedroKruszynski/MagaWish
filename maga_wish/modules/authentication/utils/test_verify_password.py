from passlib.context import CryptContext

from maga_wish.modules.authentication.utils.verify_password import verify_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def test_verify_password():
    plain_password = "mysecretpassword"
    hashed_password = pwd_context.hash(plain_password)

    assert verify_password(plain_password, hashed_password) is True
    assert verify_password("wrongpassword", hashed_password) is False
