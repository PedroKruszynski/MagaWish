from asyncio import gather

from maga_wish.modules.users.dtos import UpdateUserDTO
from maga_wish.modules.users.infra.sqlAlchemy.entities.users import User
from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository
from maga_wish.shared.infra.http.utils import SessionDep
from maga_wish.shared.infra.redis.main import RedisDefault


class UpdateUserService:
    def __init__(self, repository: UserRepository, redis_client: RedisDefault):
        self.repository = repository
        self.redis_client = redis_client

    async def update(self, session: SessionDep, userData: UpdateUserDTO) -> User | None:
        userUpdated = self.repository.update(session=session, userData=userData)

        if userUpdated:
            jsonData = userUpdated.model_dump_json()
            await gather(
                self.redis_client.set(f"user:{userUpdated.id}", jsonData),
                self.redis_client.set(f"user:{userUpdated.email}", jsonData),
            )

        return userUpdated
