from unittest.mock import AsyncMock
from uuid import uuid4
from datetime import datetime

import pytest
from fastapi import status
from tests.shared.mocks.token import bearerToken
from tests.shared.mocks.user import user
from maga_wish.modules.users.infra.http.controllers.delete_user import (
    getUserByIdService,
    deleteUserService
)

@pytest.mark.asyncio
async def test_delete_user_not_authenticated(app, client):
    async with client:
        response = await client.delete(f"/users/{user.id}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_delete_user_not_found(app, client, mock_delete_user_service):
    mock_service = AsyncMock()
    mock_service.getUserById = AsyncMock(return_value=None)

    app.dependency_overrides[getUserByIdService] = lambda: mock_service
    app.dependency_overrides[deleteUserService] = lambda: mock_delete_user_service

    async with client:
        response = await client.delete(f"/users/{user.id}", headers=bearerToken)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_delete_user_already_deleted(app, client, mock_delete_user_service):
    mock_service = AsyncMock()
    mock_service.getUserById = AsyncMock(return_value=user)
    user.deleted_at = datetime.now()

    app.dependency_overrides[getUserByIdService] = lambda: mock_service
    app.dependency_overrides[deleteUserService] = lambda: mock_delete_user_service

    async with client:
        response = await client.delete(f"/users/{user.id}", headers=bearerToken)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "User already deleted"


@pytest.mark.asyncio
async def test_delete_user_success(app, client, mock_get_user_by_id_service, mock_delete_user_service):
    mock_service = AsyncMock()
    user.deleted_at = None
    mock_service.getUserById = AsyncMock(return_value=user)

    app.dependency_overrides[getUserByIdService] = lambda: mock_service
    app.dependency_overrides[deleteUserService] = lambda: mock_delete_user_service
    
    async with client:
        response = await client.delete(f"/users/{user.id}", headers=bearerToken)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "User Deleted"
    assert response.json()["success"] is True
