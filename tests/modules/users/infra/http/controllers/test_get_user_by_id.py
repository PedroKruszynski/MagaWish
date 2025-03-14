from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import status

from maga_wish.modules.users.infra.http.controllers.get_user_by_id import (
    getUserByIdService,
)
from tests.shared.mocks.token import bearerToken
from tests.shared.mocks.user import user


@pytest.mark.asyncio
async def test_get_user_by_id_not_authenticated(
    app, client, mock_get_user_by_id_service
):
    user_id = uuid4()
    app.dependency_overrides[getUserByIdService] = lambda: mock_get_user_by_id_service

    async with client:
        response = await client.get(f"/users/{user_id}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_user_by_id_success(app, client, mock_get_user_by_id_service):
    app.dependency_overrides[getUserByIdService] = lambda: mock_get_user_by_id_service

    async with client:
        response = await client.get(f"/users/{user.id}", headers=bearerToken)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == str(user.id)


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(app, client):
    mock_service = AsyncMock()
    mock_service.getUserById = AsyncMock(return_value=None)

    app.dependency_overrides[getUserByIdService] = lambda: mock_service

    async with client:
        response = await client.get(f"/users/{user.id}", headers=bearerToken)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"
