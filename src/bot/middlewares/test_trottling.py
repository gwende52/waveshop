import pytest
from unittest.mock import AsyncMock, Mock
from src.core.constants import CONTAINER_KEY, USER_KEY
from src.bot.middlewares import ThrottlingMiddleware
from src.infrastructure.database.models.dto import UserDto


@pytest.mark.asyncio
async def test_throttling_middleware_allows_first_request():
    middleware = ThrottlingMiddleware(ttl=1.0)
    handler = AsyncMock(return_value="handled")

    # Используем мок вместо создания UserDto
    user = Mock()
    user.telegram_id = 123

    event_mock = Mock()

    container = AsyncMock()
    notification_service = AsyncMock()
    container.get = AsyncMock(return_value=notification_service)

    data = {CONTAINER_KEY: container, USER_KEY: user}

    result = await middleware.middleware_logic(handler, event_mock, data)

    handler.assert_called_once_with(event_mock, data)
    assert result == "handled"
    # Проверим, что пользователь добавлен в кэш
    assert user.telegram_id in middleware.cache


@pytest.mark.asyncio
async def test_throttling_middleware_blocks_repeated_request():
    middleware = ThrottlingMiddleware(ttl=1.0)
    handler = AsyncMock()

    user = Mock()
    user.telegram_id = 123

    event_mock = Mock()

    container = AsyncMock()
    notification_service = AsyncMock()
    container.get = AsyncMock(return_value=notification_service)

    data = {CONTAINER_KEY: container, USER_KEY: user}

    # Добавим пользователя в кэш вручную
    middleware.cache[user.telegram_id] = None

    result = await middleware.middleware_logic(handler, event_mock, data)

    handler.assert_not_called()
    assert result is None
    # Проверим, что сервис уведомлений был вызван
    notification_service.notify_user.assert_called_once()


@pytest.mark.asyncio
async def test_throttling_middleware_ttl_expires():
    middleware = ThrottlingMiddleware(ttl=0.01)  # Очень маленький TTL для теста
    handler = AsyncMock(return_value="handled")

    user = Mock()
    user.telegram_id = 123

    event_mock = Mock()

    container = AsyncMock()
    notification_service = AsyncMock()
    container.get = AsyncMock(return_value=notification_service)

    data = {CONTAINER_KEY: container, USER_KEY: user}

    # Первый вызов - должен пройти
    result1 = await middleware.middleware_logic(handler, event_mock, data)
    assert result1 == "handled"
    handler.assert_called_once()

    # Обнулим вызовы
    handler.reset_mock()

    # Ждем истечения TTL
    import asyncio

    await asyncio.sleep(0.02)

    # Второй вызов - должен пройти, так как TTL истёк
    result2 = await middleware.middleware_logic(handler, event_mock, data)
    assert result2 == "handled"
    handler.assert_called_once()


def test_throttling_middleware_attributes():
    assert ThrottlingMiddleware.__event_types__ is not None


def test_middleware_logic_exists():
    assert callable(getattr(ThrottlingMiddleware, "middleware_logic", None))
