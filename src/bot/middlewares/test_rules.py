import pytest
from unittest.mock import AsyncMock, Mock
from aiogram.types import Message, User
from src.core.constants import CONTAINER_KEY

# Импортируем напрямую из файла, чтобы избежать циклического импорта
from src.bot.middlewares.access import AccessMiddleware


@pytest.mark.asyncio
async def test_middleware_blocks_bot_user():
    middleware = AccessMiddleware()
    handler = AsyncMock()
    user = User(id=123, is_bot=True, first_name="Bot")

    # Используем мок-объект вместо Message
    event_mock = Mock()
    event_mock.from_user = user

    data = {CONTAINER_KEY: AsyncMock()}

    result = await middleware.middleware_logic(handler, event_mock, data)

    handler.assert_not_called()
    assert result is None


@pytest.mark.asyncio
async def test_middleware_blocks_no_user():
    middleware = AccessMiddleware()
    handler = AsyncMock()

    # Используем мок-объект без from_user
    event_mock = Mock()
    event_mock.from_user = None

    data = {CONTAINER_KEY: AsyncMock()}

    result = await middleware.middleware_logic(handler, event_mock, data)

    handler.assert_not_called()
    assert result is None


@pytest.mark.asyncio
async def test_middleware_allows_access():
    middleware = AccessMiddleware()
    handler = AsyncMock(return_value="handled")
    user = User(id=123, is_bot=False, first_name="RealUser")

    event_mock = Mock()
    event_mock.from_user = user

    container = AsyncMock()
    access_service = AsyncMock()
    access_service.is_access_allowed = AsyncMock(return_value=True)
    container.get = AsyncMock(return_value=access_service)

    data = {CONTAINER_KEY: container}

    result = await middleware.middleware_logic(handler, event_mock, data)

    handler.assert_called_once_with(event_mock, data)
    assert result == "handled"


@pytest.mark.asyncio
async def test_middleware_denies_access():
    middleware = AccessMiddleware()
    handler = AsyncMock()
    user = User(id=123, is_bot=False, first_name="RealUser")

    event_mock = Mock()
    event_mock.from_user = user

    container = AsyncMock()
    access_service = AsyncMock()
    access_service.is_access_allowed = AsyncMock(return_value=False)
    container.get = AsyncMock(return_value=access_service)

    data = {CONTAINER_KEY: container}

    result = await middleware.middleware_logic(handler, event_mock, data)

    handler.assert_not_called()
    assert result is None
