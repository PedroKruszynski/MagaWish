from fastapi import APIRouter

from maga_wish.modules.users.infra.http.routes.main import router as users_router
from maga_wish.modules.authentication.infra.http.routes.main import router as authentication_router
from maga_wish.modules.wishlists.infra.http.routes.main import router as wishlist_router

api_router = APIRouter()

api_router.include_router(users_router)
api_router.include_router(authentication_router)
api_router.include_router(wishlist_router)
