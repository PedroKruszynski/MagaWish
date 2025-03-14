import pytest
from unittest.mock import AsyncMock, MagicMock

from maga_wish.modules.users.services import GetUserByEmailService
from maga_wish.modules.authentication.utils.verify_password import pwd_context

@pytest.fixture
def mock_get_user_by_email_service():
    service = AsyncMock(spec=GetUserByEmailService)
    hashed_password = pwd_context.hash("password")
    mock_user = MagicMock(id=1, email="test@example.com", hashed_password=hashed_password)
    service.getUser = AsyncMock(return_value=mock_user)
    return service