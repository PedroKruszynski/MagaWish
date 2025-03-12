from asyncio import gather

from maga_wish.shared.infra.redis.main import RedisDefault
from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository
from maga_wish.modules.users.dtos import CreateUserDTO
from maga_wish.modules.users.infra.sqlAlchemy.entities.users import User
from maga_wish.shared.infra.http.utils import SessionDep

class CreateUserService:
    def __init__(self, repository: UserRepository, redis_client: RedisDefault):
        self.repository = repository
        self.redis_client = redis_client

    async def create(self, session: SessionDep, user: CreateUserDTO) -> User:
        userCreated = self.repository.create(session=session, userData=user)
        jsonData = userCreated.model_dump_json()
        
        await gather(
            self.redis_client.set(f"user:{userCreated.id}", jsonData),
            self.redis_client.set(f"user:{userCreated.email}", jsonData)
        )

        return userCreated
