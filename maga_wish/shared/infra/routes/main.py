from fastapi import APIRouter

from maga_wish.modules.users.infra.http.routes.main import router as users_router
# from maga_wish.shared.environment import settings

api_router = APIRouter()

api_router.include_router(users_router)


# if settings.ENVIRONMENT == "local":
    # api_router.include_router(private.router)