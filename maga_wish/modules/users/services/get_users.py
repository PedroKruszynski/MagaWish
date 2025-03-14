from maga_wish.modules.users.dtos import GetUsersDTO
from maga_wish.modules.users.infra.sqlAlchemy.entities.users import User
from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository
from maga_wish.shared.infra.http.utils import SessionDep


class GetUsersService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def getUsers(
        self, session: SessionDep, data: GetUsersDTO
    ) -> list[User] | None:
        return self.repository.getUsers(session=session, data=data)
