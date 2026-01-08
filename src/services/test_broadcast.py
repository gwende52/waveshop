# src/services/test_broadcast.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram import Bot
from fluentogram import TranslatorHub
from redis.asyncio import Redis

from src.core.config import AppConfig
from src.core.enums import BroadcastAudience
from src.infrastructure.database import UnitOfWork
from src.infrastructure.redis import RedisRepository
from src.services.broadcast import BroadcastService


@pytest.fixture
def broadcast_service():
    # Создаём моки для вложенных репозиториев
    mock_users_repo = AsyncMock()
    mock_subscriptions_repo = AsyncMock()
    mock_plans_repo = AsyncMock()
    mock_broadcasts_repo = AsyncMock()

    # Собираем фейковый repository facade
    mock_repository = MagicMock()
    mock_repository.users = mock_users_repo
    mock_repository.subscriptions = mock_subscriptions_repo
    mock_repository.plans = mock_plans_repo
    mock_repository.broadcasts = mock_broadcasts_repo

    # Мок UnitOfWork с настроенным repository
    mock_uow = AsyncMock(spec=UnitOfWork)
    mock_uow.repository = mock_repository

    return BroadcastService(
        config=AppConfig.get(),
        bot=AsyncMock(spec=Bot),
        redis_client=AsyncMock(spec=Redis),
        redis_repository=AsyncMock(spec=RedisRepository),
        translator_hub=MagicMock(spec=TranslatorHub),
        uow=mock_uow,
    )


@pytest.mark.asyncio
async def test_get_audience_count_all(broadcast_service):
    """Тестирует подсчёт аудитории BroadcastAudience.ALL."""
    # Arrange
    broadcast_service.uow.repository.users._count = AsyncMock(return_value=42)

    # Act
    result = await broadcast_service.get_audience_count(
        audience=BroadcastAudience.ALL
    )

    # Assert
    assert result == 42
    broadcast_service.uow.repository.users._count.assert_awaited_once()
