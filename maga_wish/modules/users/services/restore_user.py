from asyncio import gather

from maga_wish.modules.users.dtos import RestoreUserDTO
from maga_wish.modules.users.infra.sqlAlchemy.entities.users import User
from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository
from maga_wish.shared.infra.http.utils import SessionDep
from maga_wish.shared.infra.redis.main import RedisDefault


class RestoreUserService:
    def __init__(self, repository: UserRepository, redisClient: RedisDefault):
        self.repository = repository
        self.redisClient = redisClient

    async def restoreUser(
        self, session: SessionDep, data: RestoreUserDTO
    ) -> User | None | bool:
        userRestored = self.repository.restoreUser(session=session, data=data)

        if userRestored:
            jsonData = userRestored.model_dump_json()
            await gather(
                self.redisClient.set(f"user:{userRestored.id}", jsonData),
                self.redisClient.set(f"user:{userRestored.email}", jsonData),
            )

        return userRestored
