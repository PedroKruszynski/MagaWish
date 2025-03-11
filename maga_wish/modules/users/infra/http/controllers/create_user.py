from typing import Any
from fastapi import APIRouter, Depends

from maga_wish.modules.users.dtos.create_user_dto import CreateUserDTO
from maga_wish.modules.users.dtos.user import User
from maga_wish.modules.users.services import CreateUserService
from maga_wish.shared.infra.http.utils import SessionDep
from maga_wish.modules.users.infra.sqlAlchemy.repository.main import UserRepository

# from fastapi import HTTPException

router = APIRouter()

def get_user_service(
    user_repository: UserRepository = Depends(UserRepository)
) -> CreateUserService:
    return CreateUserService(user_repository)

@router.post("/", response_model=User)
async def get_user_by_id(
    *,
    session: SessionDep,
    user: CreateUserDTO,
    create_user_service: CreateUserService = Depends(get_user_service)
) -> Any:
    """
    Create new user
    """
    print(session)
    print(user)

    response = await create_user_service.create(session, user)

    # t = User
    # t.name = 't'
    # t.email = 'p@gmail.com'
    # t.id = '618b3eee-aafa-46a6-ba18-998da1615571'
    # t.created_at = datetime.now()

    print(response)
    return response
    # user = session.get(User, user_id)
    # if user == current_user:
    #     return user
    # if not current_user.is_superuser:
    #     raise HTTPException(
    #         status_code=403,
    #         detail="The user doesn't have enough privileges",
    #     )
    # return user