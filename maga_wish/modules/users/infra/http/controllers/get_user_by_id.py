import uuid
from typing import Any

from maga_wish.modules.users.dtos.user import User
from maga_wish.shared.infra.http.utils import (
    SessionDep,
    CurrentUser
)
# from fastapi import HTTPException
from fastapi import APIRouter

router = APIRouter()

@router.get("/{user_id}", response_model=User)
def get_user_by_id(
    user_id: uuid.UUID, session: SessionDep, current_user: CurrentUser
) -> Any:
    """
    Get a specific user by id.
    """
    print(user_id)
    print(session)
    print(current_user)

    t = User
    t.name = 't'
    t.email = 'dasdas'
    t.id = '618b3eee-aafa-46a6-ba18-998da1615571'

    return t
    # print(current_user)
    # user = session.get(User, user_id)
    # if user == current_user:
    #     return user
    # if not current_user.is_superuser:
    #     raise HTTPException(
    #         status_code=403,
    #         detail="The user doesn't have enough privileges",
    #     )
    # return user