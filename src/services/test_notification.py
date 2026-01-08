# src/services/test_notification_service.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram import Bot
from fluentogram import TranslatorHub
from redis.asyncio import Redis

from src.core.config import AppConfig
from src.core.enums import Locale, UserNotificationType
from src.infrastructure.database.models.dto import UserDto
from src.infrastructure.redis import RedisRepository
from src.core.utils.message_payload import MessagePayload
from src.services.notification import NotificationService


@pytest.fixture
def notification_service():
    mock_translator = MagicMock()
    mock_translator.get = MagicMock(return_value="Test message")

    mock_hub = MagicMock(spec=TranslatorHub)
    mock_hub.get_translator_by_locale = MagicMock(return_value=mock_translator)

    return NotificationService(
        config=AppConfig.get(),
        bot=AsyncMock(spec=Bot),
        redis_client=AsyncMock(spec=Redis),
        redis_repository=AsyncMock(spec=RedisRepository),
        translator_hub=mock_hub,
        user_service=AsyncMock(),
        settings_service=AsyncMock(),
    )


@pytest.mark.asyncio
async def test_notify_user_success_with_type(notification_service):
    """Тестирует успешную отправку уведомления с указанием типа."""
    # Arrange
    user = UserDto(telegram_id=12345, name="Test User", language=Locale.EN)
    payload = MessagePayload(i18n_key="test.key")

    # Используем реальное значение из enum (замените на ваше!)
    ntf_type = next(
        iter(UserNotificationType)
    )  # ← безопасный способ взять любое значение

    notification_service.settings_service.is_notification_enabled = AsyncMock(
        return_value=True
    )
    notification_service._send_message = AsyncMock(
        return_value=MagicMock(message_id=999)
    )

    # Act
    result = await notification_service.notify_user(
        user=user, payload=payload, ntf_type=ntf_type
    )

    # Assert
    assert result is not None
    notification_service.settings_service.is_notification_enabled.assert_awaited_once_with(
        ntf_type
    )
    notification_service._send_message.assert_awaited_once_with(
        user=user, payload=payload
    )


@pytest.mark.asyncio
async def test_notify_user_disabled_notification_type(notification_service):
    """Тестирует, что уведомление не отправляется, если тип отключён."""
    user = UserDto(telegram_id=12345, name="Test User", language=Locale.EN)
    payload = MessagePayload(i18n_key="test.key")
    ntf_type = next(iter(UserNotificationType))  # ← реальное значение

    notification_service.settings_service.is_notification_enabled = AsyncMock(
        return_value=False
    )

    with patch.object(
        notification_service, "_send_message", new=AsyncMock()
    ) as mock_send:
        result = await notification_service.notify_user(
            user=user, payload=payload, ntf_type=ntf_type
        )

    assert result is None
    notification_service.settings_service.is_notification_enabled.assert_awaited_once_with(
        ntf_type
    )
    mock_send.assert_not_called()


@pytest.mark.asyncio
async def test_notify_user_success_with_type(notification_service):
    """Тестирует успешную отправку уведомления с указанием типа."""
    # Arrange
    user = UserDto(telegram_id=12345, name="Test User", language=Locale.EN)
    payload = MessagePayload(i18n_key="test.key")

    ntf_type = next(iter(UserNotificationType))

    notification_service.settings_service.is_notification_enabled = AsyncMock(
        return_value=True
    )

    # Мокаем _send_message
    with patch.object(
        notification_service, "_send_message", new=AsyncMock()
    ) as mock_send:
        # Act
        result = await notification_service.notify_user(
            user=user, payload=payload, ntf_type=ntf_type
        )

        # Assert
        assert result is not None
        notification_service.settings_service.is_notification_enabled.assert_awaited_once_with(
            ntf_type
        )
        mock_send.assert_awaited_once_with(user, payload)  # ← позиционные аргументы!
