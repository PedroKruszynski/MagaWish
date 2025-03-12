from asyncio import gather

from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository
from maga_wish.modules.users.dtos import GetUserByEmail
from maga_wish.modules.users.infra.sqlAlchemy.entities.users import User
from maga_wish.shared.infra.http.utils import SessionDep
from maga_wish.shared.infra.redis.main import RedisDefault

class GetUserByEmailService:
    def __init__(self, repository: UserRepository, redisClient: RedisDefault):
        self.repository = repository
        self.redisClient = redisClient

    async def getUser(self, session: SessionDep, user: GetUserByEmail) -> User | None:
        userExistInRedis = await self.redisClient.get(f"user:{user.email}")
        if userExistInRedis:
            return userExistInRedis

        userExist = self.repository.getUserByEmail(session=session, user_data=user)
        jsonData = userExist.model_dump_json()
        if userExist:
            await gather(
                self.redisClient.set(f"user:{userExist.id}", jsonData),
                self.redisClient.set(f"user:{userExist.email}", jsonData)
            )

        return userExist
