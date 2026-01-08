# src/services/test_command_service.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram import Bot
from fluentogram import TranslatorHub
from redis.asyncio import Redis

from src.core.config import AppConfig
from src.core.enums import Command, Locale
from src.infrastructure.redis import RedisRepository
from src.services.command import CommandService


@pytest.fixture
def command_service():
    """Создаём CommandService с замоканными зависимостями."""
    mock_translator = MagicMock()
    mock_translator.get = MagicMock(side_effect=lambda key: f"desc_{key}")

    mock_hub = MagicMock(spec=TranslatorHub)
    mock_hub.get_translator_by_locale = MagicMock(return_value=mock_translator)

    return CommandService(
        config=AppConfig.get(),  # Используем мок из conftest.py
        bot=AsyncMock(spec=Bot),
        redis_client=AsyncMock(spec=Redis),
        redis_repository=AsyncMock(spec=RedisRepository),
        translator_hub=mock_hub,
    )


@pytest.mark.asyncio
async def test_setup_commands_enabled(command_service):
    """Тестирует настройку команд, когда setup_commands = True."""
    # Arrange
    command_service.config.bot.setup_commands = True
    command_service.config.locales = [Locale.RU, Locale.EN]
    command_service.config.default_locale = Locale.EN

    # Мокаем успешный ответ от Telegram API
    command_service.bot.set_my_commands = AsyncMock(return_value=True)

    # Act
    await command_service.setup()

    # Assert
    # Должно быть вызвано 3 раза: ru, en, None (default)
    assert command_service.bot.set_my_commands.call_count == 3

    # Проверяем вызов для русского языка
    call_ru = command_service.bot.set_my_commands.call_args_list[0]
    assert call_ru.kwargs["language_code"] == Locale.RU
    assert len(call_ru.kwargs["commands"]) == len(Command)

    # Проверяем вызов для английского
    call_en = command_service.bot.set_my_commands.call_args_list[1]
    assert call_en.kwargs["language_code"] == Locale.EN

    # Проверяем вызов для default
    call_default = command_service.bot.set_my_commands.call_args_list[2]
    assert call_default.kwargs["language_code"] is None

    # Убеждаемся, что переводчик вызывался
    assert command_service.translator_hub.get_translator_by_locale.call_count == 3


@pytest.mark.asyncio
async def test_setup_commands_disabled(command_service):
    """Тестирует, что команды не настраиваются, если setup_commands = False."""
    # Arrange
    command_service.config.bot.setup_commands = False
    command_service.bot.set_my_commands = AsyncMock()

    # Act
    await command_service.setup()

    # Assert
    command_service.bot.set_my_commands.assert_not_called()
    command_service.translator_hub.get_translator_by_locale.assert_not_called()
