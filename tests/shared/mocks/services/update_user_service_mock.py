from unittest.mock import AsyncMock

import pytest

from maga_wish.modules.users.dtos import UpdateUserDTO
from maga_wish.modules.users.services import GetUserByIdService
from tests.shared.mocks.user import user


@pytest.fixture
def mock_update_user_service():
    service = AsyncMock(spec=GetUserByIdService)

    async def update(_, userData: UpdateUserDTO):
        attrs = userData.dict(exclude_unset=True)
        updated_user = {**user.model_dump(), **attrs}
        return updated_user

    service.update = AsyncMock(side_effect=update)
    return service
