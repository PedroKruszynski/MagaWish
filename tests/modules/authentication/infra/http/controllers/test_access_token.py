from unittest.mock import AsyncMock

import pytest
from fastapi import status

from maga_wish.modules.authentication.infra.http.controllers.access_token import (
    getUserByEmailService,
)


@pytest.mark.asyncio
async def test_access_token_success(app, client, mock_get_user_by_email_service):
    app.dependency_overrides[getUserByEmailService] = (
        lambda: mock_get_user_by_email_service
    )

    async with client:
        response = await client.post(
            "/login", data={"username": "test@example.com", "password": "password"}
        )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_access_token_user_not_find(app, client):
    mock_service = AsyncMock()
    mock_service.getUser = AsyncMock(return_value=None)

    app.dependency_overrides[getUserByEmailService] = lambda: mock_service

    async with client:
        response = await client.post(
            "/login",
            data={"username": "wrong@example.com", "password": "wrongpassword"},
        )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "E-mail or password incorrect"


@pytest.mark.asyncio
async def test_access_token_invalid_credentials(
    app, client, mock_get_user_by_email_service
):
    app.dependency_overrides[getUserByEmailService] = (
        lambda: mock_get_user_by_email_service
    )

    async with client:
        response = await client.post(
            "/login",
            data={"username": "wrong@example.com", "password": "wrongpassword"},
        )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "E-mail or password incorrect"
