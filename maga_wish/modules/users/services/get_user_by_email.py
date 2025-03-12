from asyncio import gather
from redis.asyncio.client import Redis

from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository
from maga_wish.modules.users.dtos import GetUserByEmailDTO
from maga_wish.modules.users.infra.sqlAlchemy.entities.users import User
from maga_wish.shared.infra.http.utils import SessionDep

class GetUserByEmailService:
    def __init__(self, repository: UserRepository, redisClient: Redis):
        self.repository = repository
        self.redisClient = redisClient

    async def getUser(self, session: SessionDep, user: GetUserByEmailDTO) -> User | None:
        userExistInRedis = await self.redisClient.get(f"user:{user.email}")
        if userExistInRedis:
            return userExistInRedis

        userExist = self.repository.getUserByEmail(session=session, user_data=user)
        if userExist:
            jsonData = userExist.model_dump_json()
            await gather(
                self.redisClient.set(f"user:{userExist.id}", jsonData),
                self.redisClient.set(f"user:{userExist.email}", jsonData)
            )

        return userExist
