import uuid
from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
# @router.get("/{user_id}", response_model=UserPublic)
def get_users(
    # session: SessionDep, skip: int = 0, limit: int = 100
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