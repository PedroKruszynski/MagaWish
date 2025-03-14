import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from maga_wish.modules.authentication.infra.http.routes.main import (
    router as authentication_router,
)
from maga_wish.modules.users.infra.http.routes.main import router as users_router
from maga_wish.modules.wishlists.infra.http.routes.main import router as wishlist_router


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(users_router)
    app.include_router(authentication_router)
    app.include_router(wishlist_router)
    return app


@pytest.fixture
def client(app):
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
