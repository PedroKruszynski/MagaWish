from asyncio import gather

from maga_wish.shared.infra.redis.main import RedisDefault
from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository
from maga_wish.modules.users.dtos import DeleteUserDTO
from maga_wish.modules.users.infra.sqlAlchemy.entities.users import User
from maga_wish.shared.infra.http.utils import SessionDep

class DeleteUserService:
    def __init__(self, repository: UserRepository, redisClient: RedisDefault):
        self.repository = repository
        self.redisClient = redisClient

    async def deleteUser(self, session: SessionDep, data: DeleteUserDTO) -> bool:
        userDeleted = self.repository.deleteUser(session=session, data=data)

        if userDeleted:
            await gather(
                self.redisClient.remove(f"user:{data.id}"),
                self.redisClient.remove(f"user:{data.email}")
            )

        return userDeleted
