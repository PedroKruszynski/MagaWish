from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime, timezone

from maga_wish.modules.users.infra.sqlAlchemy.entities.users import User
from maga_wish.modules.users.dtos import (
    GetUserByEmailDTO,
    CreateUserDTO,
    GetUsersDTO,
    GetUserByIdDTO,
    DeleteUserDTO,
    UpdateUserDTO
)
from maga_wish.modules.authentication.utils.get_password_hash import get_password_hash

class UserRepository:
    def create(self, *, session: Session, userData: CreateUserDTO) -> User:
        user = User.model_validate(
            userData, update={"hashed_password": get_password_hash(userData.password)}
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    
    def getUserByEmail(self, *, session: Session, userData: GetUserByEmailDTO) -> User | None: 
        query = select(User).where(User.email == userData.email)
        user = session.exec(query).first()
        return user

    def getUserById(self, *, session: Session, userData: GetUserByIdDTO) -> User | None: 
        query = select(User).where(User.id == userData.id)
        user = session.exec(query).first()
        return user
    
    def getUsers(self, *, session: Session, data: GetUsersDTO) -> Optional[List[User]]: 
        query = select(User).limit(data.limit).offset(data.limit * (data.page - 1))
        users = session.exec(query).all()

        return users if users else []
    
    def deleteUser(self, *, session: Session, data: DeleteUserDTO) -> bool: 
        user = self.getUserById(session=session, userData=GetUserByIdDTO(id=data.id))

        user.deleted_at = datetime.now(timezone.utc)

        if user:
            session.delete(user)
            session.commit()
            return True
        return False
    
    def update(self, *, session: Session, userData: UpdateUserDTO) -> User | None:
        user = self.getUserById(session=session, userData=GetUserByIdDTO(id=userData.id))

        if not user:
            return None

        userUpdate = userData.model_dump(exclude_unset=True)

        extra_data = {}
        if "password" in userUpdate:
            password = userUpdate["password"]
            hashed_password = get_password_hash(password)
            extra_data["hashed_password"] = hashed_password

        extra_data["updated_at"] = datetime.now(timezone.utc)

        for field, value in userUpdate.items():
            setattr(user, field, value)

        for field, value in extra_data.items():
            setattr(user, field, value)

        session.commit()
        session.refresh(user)

        return user