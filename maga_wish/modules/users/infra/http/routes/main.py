from fastapi import APIRouter

from maga_wish.modules.users.infra.http.controllers import (
    get_user_by_id,
    get_users,
    create_user
)

router = APIRouter(prefix="/users", tags=["users"])

router.include_router(get_user_by_id)
router.include_router(get_users)
router.include_router(create_user)
