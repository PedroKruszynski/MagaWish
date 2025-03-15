from datetime import datetime
from uuid import uuid4

from maga_wish.modules.authentication.utils.get_password_hash import get_password_hash
from maga_wish.modules.users.dtos import CreateUserDTO
from maga_wish.modules.users.infra.sqlAlchemy.entities.users import User

dataToCreateUser = CreateUserDTO(
    email="user_test@test.com",
    password="teste",
    name="user_test",
)

user = User(
    id=uuid4(),
    name=dataToCreateUser.name,
    email=dataToCreateUser.email,
    created_at=datetime.now(),
    hashed_password=get_password_hash(dataToCreateUser.password),
    deleted_at=None,
)
