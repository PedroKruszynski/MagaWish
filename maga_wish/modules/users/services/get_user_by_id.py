from asyncio import gather

from maga_wish.shared.infra.redis.main import RedisDefault
from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository
from maga_wish.modules.users.dtos import GetUserByIdDTO
from maga_wish.modules.users.infra.sqlAlchemy.entities.users import User
from maga_wish.shared.infra.http.utils import SessionDep

class GetUserByIdService:
    def __init__(self, repository: UserRepository, redisClient: RedisDefault):
        self.repository = repository
        self.redisClient = redisClient

    async def getUserById(self, session: SessionDep, user: GetUserByIdDTO) -> User | None:
        userExistInRedis = await self.redisClient.get(f"user:{user.id}")
        if userExistInRedis:
            return User(**userExistInRedis)

        userExist = self.repository.getUserById(session=session, user_data=user)
        if userExist:
            jsonData = userExist.model_dump_json()
            await gather(
                self.redisClient.set(f"user:{userExist.id}", jsonData),
                self.redisClient.set(f"user:{userExist.email}", jsonData)
            )

        return userExist
