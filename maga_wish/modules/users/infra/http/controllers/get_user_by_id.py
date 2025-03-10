import uuid
from typing import Any

# from fastapi import HTTPException
from fastapi import APIRouter

router = APIRouter()


@router.get("/{user_id}")
# @router.get("/{user_id}", response_model=UserPublic)
def get_user_by_id(
    # user_id: uuid.UUID, session: SessionDep, current_user: CurrentUser
    user_id: uuid.UUID
) -> Any:
    """
    Get a specific user by id.
    """
    # user = session.get(User, user_id)
    # if user == current_user:
    #     return user
    # if not current_user.is_superuser:
    #     raise HTTPException(
    #         status_code=403,
    #         detail="The user doesn't have enough privileges",
    #     )
    # return user