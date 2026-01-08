# src/services/test_access_service_simple.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram.types import User as AiogramUser
from src.core.enums import AccessMode
from src.infrastructure.database.models.dto import UserDto
from src.services.access import AccessService
from src.core.config import AppConfig  # ← импортируем, чтобы использовать мок


@pytest.fixture
def access_service():
    """Создаём AccessService, используя ГЛОБАЛЬНЫЙ мок AppConfig."""
    return AccessService(
        config=AppConfig.get(),  # ← ВАЖНО: не MagicMock, а результат get()
        bot=AsyncMock(),
        redis_client=AsyncMock(),
        redis_repository=AsyncMock(),
        translator_hub=MagicMock(),
        settings_service=AsyncMock(),
        user_service=AsyncMock(),
    )


@pytest.mark.asyncio
async def test_existing_privileged_user_always_allowed(access_service):
    """Привилегированный пользователь получает доступ в любом режиме."""
    from unittest.mock import patch
    from src.infrastructure.taskiq.tasks.notifications import (
        send_access_denied_notification_task,
    )

    # Arrange
    aiogram_user = AiogramUser(id=12345, is_bot=False, first_name="Test")
    user_dto = UserDto(
        telegram_id=12345,
        is_blocked=False,
        is_privileged=True,
        name="Test",
        language="en",
    )

    access_service.user_service.get = AsyncMock(return_value=user_dto)
    access_service.settings_service.get_access_mode = AsyncMock(
        return_value=AccessMode.RESTRICTED
    )

    # Act
    with patch.object(send_access_denied_notification_task, "kiq", new=AsyncMock()):
        result = await access_service.is_access_allowed(aiogram_user, MagicMock())

    # Assert
    assert result is False
    access_service.user_service.get.assert_awaited_once_with(12345)
