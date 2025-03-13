from fastapi import APIRouter

from maga_wish.modules.wishlists.infra.http.controllers import (
    get_wishlist_by_user_id
)

router = APIRouter(prefix="/wishlist", tags=["wishlist"])

router.include_router(get_wishlist_by_user_id)

