from sqlmodel import Session

from maga_wish.modules.users.infra.sqlAlchemy.entities.users import User
from maga_wish.modules.users.dtos.create_user_dto import CreateUserDTO
from maga_wish.modules.authentication.service.get_password_hash import get_password_hash

class UserRepository:
    def create(self, *, session: Session, user_data: CreateUserDTO) -> User:
        user = User.model_validate(
            user_data, update={"hashed_password": get_password_hash(user_data.password)}
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user