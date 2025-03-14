from asyncio import gather

from maga_wish.modules.users.dtos import DeleteUserDTO
from maga_wish.modules.users.dtos.user import User
from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository
from maga_wish.shared.infra.http.utils import SessionDep
from maga_wish.shared.infra.redis.main import RedisDefault


class DeleteUserService:
    def __init__(self, repository: UserRepository, redisClient: RedisDefault):
        self.repository = repository
        self.redisClient = redisClient

    async def deleteUser(
        self, session: SessionDep, data: DeleteUserDTO
    ) -> User | None | bool:
        userDeleted = self.repository.deleteUser(session=session, data=data)

        if userDeleted:
            await gather(
                self.redisClient.remove(f"user:{userDeleted.id}"),
                self.redisClient.remove(f"user:{userDeleted.email}"),
            )

        return userDeleted
