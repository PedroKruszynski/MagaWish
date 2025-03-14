import pytest
from redis import Redis
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI, status
from unittest.mock import AsyncMock, MagicMock

from maga_wish.modules.authentication.infra.http.routes.main import router
from maga_wish.modules.users.services import GetUserByEmailService
from maga_wish.modules.authentication.infra.http.controllers.access_token import getUserByEmailService
from maga_wish.modules.authentication.utils.verify_password import pwd_context

@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(router)
    return app

@pytest.fixture
def client(app):
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")

@pytest.fixture
def mock_get_user_by_email_service():
    service = AsyncMock(spec=GetUserByEmailService)
    hashed_password = pwd_context.hash("password")
    mock_user = MagicMock(id=1, email="test@example.com", hashed_password=hashed_password)
    service.getUser = AsyncMock(return_value=mock_user)
    return service

@pytest.mark.asyncio
async def test_access_token_success(app, client, mock_get_user_by_email_service):
    app.dependency_overrides[getUserByEmailService] = lambda: mock_get_user_by_email_service

    async with client:
        response = await client.post("/login", data={
            "username": "test@example.com",
            "password": "password"
        })
    
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_access_token_invalid_credentials(app, client, mock_get_user_by_email_service):
    app.dependency_overrides[getUserByEmailService] = lambda: mock_get_user_by_email_service

    async with client:
        response = await client.post("/login", data={
            "username": "wrong@example.com",
            "password": "wrongpassword"
        })
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "E-mail or password incorrect"