# tests/services/test_subscription_service.py
import pytest
from unittest.mock import AsyncMock, MagicMock

from src.core.config import AppConfig
from src.services.subscription import SubscriptionService
from src.infrastructure.database import UnitOfWork


@pytest.fixture
def mock_uow():
    uow = MagicMock(spec=UnitOfWork)
    uow.repository = MagicMock()
    uow.repository.subscriptions = AsyncMock()
    return uow


@pytest.fixture
def subscription_service(mock_uow):
    # Минимальный набор зависимостей (остальное не нужно для этого метода)
    return SubscriptionService(
        config=MagicMock(spec=AppConfig),
        bot=MagicMock(),
        redis_client=MagicMock(),
        redis_repository=MagicMock(),
        translator_hub=MagicMock(),
        uow=mock_uow,
        user_service=MagicMock(),
    )


class TestHasAnySubscription:
    @pytest.mark.asyncio
    async def test_returns_true_when_user_has_subscriptions(
        self, subscription_service, mock_uow
    ):
        # Arrange
        user = MagicMock()
        user.telegram_id = 12345
        mock_uow.repository.subscriptions._count.return_value = 2  # 2 подписки

        # Act
        result = await subscription_service.has_any_subscription(user)

        # Assert
        assert result is True
        mock_uow.repository.subscriptions._count.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_returns_false_when_user_has_no_subscriptions(
        self, subscription_service, mock_uow
    ):
        # Arrange
        user = MagicMock()
        user.telegram_id = 12345
        mock_uow.repository.subscriptions._count.return_value = 0

        # Act
        result = await subscription_service.has_any_subscription(user)

        # Assert
        assert result is False
        mock_uow.repository.subscriptions._count.assert_awaited_once()
