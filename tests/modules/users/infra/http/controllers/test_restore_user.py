from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from fastapi import status

from maga_wish.modules.users.infra.http.controllers.restore_user import (
    getUserByIdService,
    restoreUserService,
)
from tests.shared.mocks.token import bearerToken
from tests.shared.mocks.user import user


@pytest.mark.asyncio
async def test_restore_user_not_authenticated(
    app, client, mock_get_user_by_id_service, mock_restore_user_service
):
    app.dependency_overrides[getUserByIdService] = lambda: mock_get_user_by_id_service
    app.dependency_overrides[restoreUserService] = lambda: mock_restore_user_service

    async with client:
        response = await client.put(f"/users/{user.id}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_restore_user_not_found(app, client, mock_restore_user_service):
    mock_service = AsyncMock()
    mock_service.getUserById = AsyncMock(return_value=None)

    app.dependency_overrides[getUserByIdService] = lambda: mock_service
    app.dependency_overrides[restoreUserService] = lambda: mock_restore_user_service

    async with client:
        response = await client.put(f"/users/{user.id}", headers=bearerToken)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_restore_user_not_deleted(app, client, mock_restore_user_service):
    mock_service = AsyncMock()
    mock_service.getUserById = AsyncMock(return_value=user)

    user.deleted_at = None

    app.dependency_overrides[getUserByIdService] = lambda: mock_service
    app.dependency_overrides[restoreUserService] = lambda: mock_restore_user_service

    async with client:
        response = await client.put(f"/users/{user.id}", headers=bearerToken)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "User not deleted"


@pytest.mark.asyncio
async def test_restore_user_success(app, client, mock_restore_user_service):
    mock_service = AsyncMock()

    user.deleted_at = datetime.now()

    mock_service.getUserById = AsyncMock(return_value=user)
    mock_service.restoreUser = AsyncMock(return_value=True)

    app.dependency_overrides[getUserByIdService] = lambda: mock_service
    app.dependency_overrides[restoreUserService] = lambda: mock_restore_user_service

    async with client:
        response = await client.put(f"/users/{user.id}", headers=bearerToken)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "User Restored"
    assert response.json()["success"] is True
