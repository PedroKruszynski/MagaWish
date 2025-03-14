from fastapi import APIRouter

from maga_wish.modules.wishlists.infra.http.controllers import (
    add_product_to_wishlist,
    delete_product_of_wishlist,
    get_wishlist_by_user_id,
    restore_product_of_wishlist,
)

router = APIRouter(prefix="/wishlist", tags=["wishlist"])

router.include_router(get_wishlist_by_user_id)
router.include_router(add_product_to_wishlist)
router.include_router(delete_product_of_wishlist)
router.include_router(restore_product_of_wishlist)
