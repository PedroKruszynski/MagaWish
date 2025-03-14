from fastapi import APIRouter

from maga_wish.modules.users.infra.http.controllers import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users,
    restore_user,
    update_user,
)

router = APIRouter(prefix="/users", tags=["users"])

router.include_router(get_user_by_id)
router.include_router(get_users)
router.include_router(create_user)
router.include_router(delete_user)
router.include_router(update_user)
router.include_router(restore_user)
