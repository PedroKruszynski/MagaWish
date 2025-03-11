from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository
from maga_wish.modules.users.dtos.create_user_dto import CreateUserDTO
from maga_wish.modules.users.infra.sqlAlchemy.entities.users import User
from maga_wish.shared.infra.http.utils import SessionDep

class CreateUserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create(self, session: SessionDep, user: CreateUserDTO) -> User:
        print(user)
        return await self.repository.create(session, user)
