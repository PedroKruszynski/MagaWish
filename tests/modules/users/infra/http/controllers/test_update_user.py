from unittest.mock import AsyncMock

import pytest
from fastapi import status

from maga_wish.modules.users.infra.http.controllers.update_user import (
    getUserByEmailService,
    getUserByIdService,
    updateUserService,
)
from tests.shared.mocks.token import bearerToken
from tests.shared.mocks.user import user


@pytest.mark.asyncio
async def test_update_user_not_authenticated(
    app,
    client,
    mock_get_user_by_id_service,
    mock_get_user_by_email_service,
    mock_update_user_service,
):
    app.dependency_overrides[getUserByIdService] = lambda: mock_get_user_by_id_service
    app.dependency_overrides[updateUserService] = lambda: mock_update_user_service
    app.dependency_overrides[getUserByEmailService] = (
        lambda: mock_get_user_by_email_service
    )

    async with client:
        response = await client.patch(f"/users/{user.id}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_update_user_no_data(
    app, client, mock_update_user_service, mock_get_user_by_email_service
):
    mock_service = AsyncMock()
    mock_service.getUserById = AsyncMock(return_value=user)

    app.dependency_overrides[getUserByIdService] = lambda: mock_service
    app.dependency_overrides[getUserByEmailService] = (
        lambda: mock_get_user_by_email_service
    )
    app.dependency_overrides[updateUserService] = lambda: mock_update_user_service

    user_data = {}

    async with client:
        response = await client.patch(
            f"/users/{user.id}", json=user_data, headers=bearerToken
        )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "No data provided to update the user"


@pytest.mark.asyncio
async def test_update_user_not_found(
    app, client, mock_update_user_service, mock_get_user_by_email_service
):
    mock_service = AsyncMock()
    mock_service.getUserById = AsyncMock(return_value=None)

    app.dependency_overrides[getUserByIdService] = lambda: mock_service
    app.dependency_overrides[getUserByEmailService] = (
        lambda: mock_get_user_by_email_service
    )
    app.dependency_overrides[updateUserService] = lambda: mock_update_user_service

    async with client:
        response = await client.patch(
            f"/users/{user.id}", json={"name": "New Name"}, headers=bearerToken
        )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_update_user_email_unavailable(
    app, client, mock_update_user_service, mock_get_user_by_email_service
):
    mock_service = AsyncMock()
    mock_service.getUserById = AsyncMock(return_value=user)
    mock_service.getUser = AsyncMock(return_value=user)

    app.dependency_overrides[getUserByIdService] = lambda: mock_service
    app.dependency_overrides[getUserByEmailService] = (
        lambda: mock_get_user_by_email_service
    )
    app.dependency_overrides[updateUserService] = lambda: mock_update_user_service

    user_data = {"email": "existing_email@test.com"}

    async with client:
        response = await client.patch(
            f"/users/{user.id}", json=user_data, headers=bearerToken
        )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "E-mail unavailable"


@pytest.mark.asyncio
async def test_update_user_success(
    app, client, mock_update_user_service, mock_get_user_by_email_service
):
    mock_service = AsyncMock()
    mock_service.getUserById = AsyncMock(return_value=user)

    mock_service.update = AsyncMock(return_value=user)

    app.dependency_overrides[getUserByIdService] = lambda: mock_service
    app.dependency_overrides[getUserByEmailService] = (
        lambda: mock_get_user_by_email_service
    )
    app.dependency_overrides[updateUserService] = lambda: mock_update_user_service

    user_data = {"name": "Updated Name"}

    async with client:
        response = await client.patch(
            f"/users/{user.id}", json=user_data, headers=bearerToken
        )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Updated Name"
