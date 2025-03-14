from datetime import datetime, timezone

from sqlmodel import Session, select

from maga_wish.modules.authentication.utils.get_password_hash import get_password_hash
from maga_wish.modules.users.dtos import (
    CreateUserDTO,
    DeleteUserDTO,
    GetUserByEmailDTO,
    GetUserByIdDTO,
    GetUsersDTO,
    RestoreUserDTO,
    UpdateUserDTO,
)
from maga_wish.modules.users.infra.sqlAlchemy.entities.users import User


class UserRepository:
    def create(self, *, session: Session, userData: CreateUserDTO) -> User:
        user = User.model_validate(
            userData, update={"hashed_password": get_password_hash(userData.password)}
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    def getUserByEmail(
        self, *, session: Session, userData: GetUserByEmailDTO
    ) -> User | None:
        query = select(User).where(User.email == userData.email)
        user = session.exec(query).first()
        return user

    def getUserById(self, *, session: Session, userData: GetUserByIdDTO) -> User | None:
        query = select(User).where(User.id == userData.id)
        user = session.exec(query).first()
        return user

    def getUsers(self, *, session: Session, data: GetUsersDTO) -> list[User] | None:
        query = select(User).limit(data.limit).offset(data.limit * (data.page - 1))
        users = session.exec(query).all()

        return users if users else []

    def deleteUser(
        self, *, session: Session, data: DeleteUserDTO
    ) -> User | None | bool:
        user = self.getUserById(session=session, userData=GetUserByIdDTO(id=data.id))

        if not user:
            return None

        if user.deleted_at:
            return False

        if user:
            user.deleted_at = datetime.now(timezone.utc)

            session.commit()
            session.refresh(user)

            return user

        return False

    def update(self, *, session: Session, userData: UpdateUserDTO) -> User | None:
        user = self.getUserById(
            session=session, userData=GetUserByIdDTO(id=userData.id)
        )

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

    def restoreUser(
        self, *, session: Session, data: RestoreUserDTO
    ) -> User | None | bool:
        user = self.getUserById(session=session, userData=GetUserByIdDTO(id=data.id))

        if not user:
            return None

        if not user.deleted_at:
            return False

        if user:
            user.updated_at = datetime.now(timezone.utc)
            user.deleted_at = None

            session.commit()
            session.refresh(user)

            return user

        return False
