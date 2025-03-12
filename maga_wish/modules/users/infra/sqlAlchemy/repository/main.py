from sqlmodel import Session, select
from typing import List, Optional

from maga_wish.modules.users.infra.sqlAlchemy.entities.users import User
from maga_wish.modules.users.dtos import (
    GetUserByEmailDTO,
    CreateUserDTO,
    GetUsersDTO
)
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
    
    def getUserByEmail(self, *, session: Session, user_data: GetUserByEmailDTO) -> User | None: 
        query = select(User).where(User.email == user_data.email)
        user = session.exec(query).first()
        return user
    
    def getUsers(self, *, session: Session, data: GetUsersDTO) -> Optional[List[User]]: 
        query = select(User).limit(data.limit).offset(data.limit * (data.page - 1))
        users = session.exec(query).all()

        return users if users else []