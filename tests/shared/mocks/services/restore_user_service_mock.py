from unittest.mock import AsyncMock

import pytest

from maga_wish.modules.users.services import GetUserByIdService
from tests.shared.mocks.user import user


@pytest.fixture
def mock_restore_user_service():
    service = AsyncMock(spec=GetUserByIdService)

    service.restoreUser = AsyncMock(return_value=user.model_dump())
    return service
