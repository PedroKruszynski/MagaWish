from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository
from maga_wish.modules.users.dtos import GetUserByEmail
from maga_wish.modules.users.infra.sqlAlchemy.entities.users import User
from maga_wish.shared.infra.http.utils import SessionDep

class GetUserByEmailService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def getUser(self, session: SessionDep, user: GetUserByEmail) -> User | None:
        return self.repository.getUserByEmail(session=session, user_data=user)
