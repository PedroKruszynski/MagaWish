from sqlmodel import Session

from maga_wish.modules.users.infra.sqlAlchemy.entities.users import User
from maga_wish.modules.users.dtos.create_user_dto import CreateUserDTO
from maga_wish.modules.authentication.service import get_password_hash

class UserRepository:
    def create(self, *, session: Session, user_create: CreateUserDTO) -> User:
        user = User.model_validate(
            user_create, update={"hashed_password": get_password_hash(user_create.password)}
        )
        session.add(user)
        session.commit()  # Commit to save to DB
        session.refresh(user)  # Refresh to get any auto-generated fields (like ID)
        return user

    # async def get(self, item_id: int) -> Item:
    #     async with self.db_pool.acquire() as connection:
    #         result = await connection.fetchrow("SELECT id, name, description FROM items WHERE id=$1", item_id)
    #         if result:
    #             return Item(id=result['id'], name=result['name'], description=result['description'])
    #     return None

    # async def list_all(self) -> List[Item]:
    #     async with self.db_pool.acquire() as connection:
    #         result = await connection.fetch("SELECT id, name, description FROM items")
    #         return [Item(id=row['id'], name=row['name'], description=row['description']) for row in result]
