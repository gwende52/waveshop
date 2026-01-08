# src/services/test_payment_gateway_service.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram import Bot
from fluentogram import TranslatorHub
from redis.asyncio import Redis
from uuid import UUID

from src.core.config import AppConfig
from src.core.enums import PaymentGatewayType, Locale
from src.infrastructure.database import UnitOfWork
from src.infrastructure.redis import RedisRepository
from src.infrastructure.payment_gateways import (
    BasePaymentGateway,
    PaymentGatewayFactory,
)
from src.infrastructure.database.models.dto import (
    UserDto,
    PaymentResult,
    TransactionDto,
)
from src.services.transaction import TransactionService
from src.services.subscription import SubscriptionService
from src.services.payment_gateway import PaymentGatewayService


@pytest.fixture
def payment_gateway_service():
    """Создаём PaymentGatewayService с полностью замоканными зависимостями."""
    mock_translator = MagicMock()
    mock_translator.get = MagicMock(
        side_effect=lambda key, **kwargs: f"Translated: {key}"
    )

    mock_hub = MagicMock(spec=TranslatorHub)
    mock_hub.get_translator_by_locale = MagicMock(return_value=mock_translator)

    # Мок фабрики шлюзов
    mock_gateway_instance = AsyncMock(spec=BasePaymentGateway)
    mock_gateway_instance.gateway.type = PaymentGatewayType.YOOKASSA
    mock_gateway_instance.gateway.currency = MagicMock(symbol="₽")

    mock_factory = MagicMock(spec=PaymentGatewayFactory)
    mock_factory.return_value = mock_gateway_instance

    return PaymentGatewayService(
        config=AppConfig.get(),
        bot=AsyncMock(spec=Bot),
        redis_client=AsyncMock(spec=Redis),
        redis_repository=AsyncMock(spec=RedisRepository),
        translator_hub=mock_hub,
        uow=AsyncMock(spec=UnitOfWork),
        transaction_service=AsyncMock(spec=TransactionService),
        subscription_service=AsyncMock(spec=SubscriptionService),
        payment_gateway_factory=mock_factory,
    )


@pytest.fixture
def payment_gateway_service():
    """Создаём PaymentGatewayService с полностью замоканными зависимостями."""
    mock_translator = MagicMock()
    mock_translator.get = MagicMock(
        side_effect=lambda key, **kwargs: f"Translated: {key}"
    )

    mock_hub = MagicMock(spec=TranslatorHub)
    mock_hub.get_translator_by_locale = MagicMock(return_value=mock_translator)

    # 🔑 Создаём вложенный мок gateway явно
    mock_gateway = MagicMock()
    mock_gateway.type = PaymentGatewayType.YOOKASSA
    mock_gateway.currency = MagicMock(symbol="₽")

    mock_gateway_instance = AsyncMock(spec=BasePaymentGateway)
    mock_gateway_instance.gateway = (
        mock_gateway  # ← присваиваем уже существующий объект
    )

    mock_factory = MagicMock(spec=PaymentGatewayFactory)
    mock_factory.return_value = mock_gateway_instance

    return PaymentGatewayService(
        config=AppConfig.get(),
        bot=AsyncMock(spec=Bot),
        redis_client=AsyncMock(spec=Redis),
        redis_repository=AsyncMock(spec=RedisRepository),
        translator_hub=mock_hub,
        uow=AsyncMock(spec=UnitOfWork),
        transaction_service=AsyncMock(spec=TransactionService),
        subscription_service=AsyncMock(spec=SubscriptionService),
        payment_gateway_factory=mock_factory,
    )
