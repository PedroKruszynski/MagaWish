from unittest.mock import AsyncMock

import pytest

from maga_wish.modules.users.services import GetUserByIdService
from tests.shared.mocks.user import user


@pytest.fixture
def mock_get_user_by_id_service():
    service = AsyncMock(spec=GetUserByIdService)

    service.getUserById = AsyncMock(return_value=user.model_dump())
    return service
