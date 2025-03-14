from fastapi import APIRouter

from maga_wish.modules.authentication.infra.http.controllers import access_token

router = APIRouter(tags=["authentication"])

router.include_router(access_token)
