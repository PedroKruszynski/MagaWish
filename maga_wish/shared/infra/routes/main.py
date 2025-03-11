from fastapi import APIRouter

from maga_wish.modules.users.infra.http.routes.main import router as users_router

api_router = APIRouter()

api_router.include_router(users_router)
