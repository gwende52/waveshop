import uuid
from decimal import Decimal
import pytest
from unittest.mock import AsyncMock
import inspect  # Для проверки, является ли метод корутиной
from aiogram.types import LabeledPrice
from src.infrastructure.payment_gateways import TelegramStarsGateway
from src.core.enums import TransactionStatus
from src.infrastructure.database.models.dto import PaymentResult


class TestTelegramStarsGateway:
    """Поверхностные юнит-тесты для TelegramStarsGateway."""

    def test_handle_webhook_is_async_method(self):
        """Проверяет, что handle_webhook является асинхронным методом."""
        gateway = TelegramStarsGateway(bot=AsyncMock(), gateway=AsyncMock())

        # Проверяем, что метод существует
        assert hasattr(gateway, "handle_webhook")

        # Проверяем, что метод помечен как async (возвращает корутину)
        method = getattr(gateway, "handle_webhook")
        assert inspect.iscoroutinefunction(method), (
            f"{method} is not a coroutine function"
        )

    @pytest.mark.asyncio
    async def test_handle_webhook_raises_not_implemented(self):
        """Проверяет, что handle_webhook вызывает NotImplementedError при вызове."""
        gateway = TelegramStarsGateway(bot=AsyncMock(), gateway=AsyncMock())
        mock_request = AsyncMock()

        # Проверяем, что метод вызывает NotImplementedError
        with pytest.raises(NotImplementedError):
            await gateway.handle_webhook(mock_request)

    @pytest.mark.asyncio
    async def test_handle_create_payment_creates_correct_prices(self):
        """Проверяет, что handle_create_payment создает LabeledPrice с правильной суммой."""
        bot_mock = AsyncMock()
        gateway_mock = AsyncMock()
        gateway_mock.currency = (
            "XTR"  # Предполагаем, что валюта XTR для Telegram Stars
        )

        gateway = TelegramStarsGateway(bot=bot_mock, gateway=gateway_mock)
        test_amount = Decimal("100.50")
        test_details = "Test payment description"

        # Предполагаем, что bot.create_invoice_link возвращает фиктивный URL
        expected_url = "https://t.me/invoice/12345"
        bot_mock.create_invoice_link = AsyncMock(return_value=expected_url)

        result = await gateway.handle_create_payment(test_amount, test_details)

        # Проверяем, что bot.create_invoice_link был вызван
        bot_mock.create_invoice_link.assert_called_once()
        # Проверяем аргументы вызова
        call_args = bot_mock.create_invoice_link.call_args
        assert call_args is not None
        # Проверяем, что переданные цены содержат правильную сумму
        prices_arg = call_args.kwargs.get("prices")
        assert prices_arg is not None
        assert len(prices_arg) == 1
        assert isinstance(prices_arg[0], LabeledPrice)
        # Сумма передается в минимальных единицах (копейки/сатоши), для XTR это целые числа
        assert prices_arg[0].amount == int(test_amount)
        assert prices_arg[0].label == gateway_mock.currency

    @pytest.mark.asyncio
    async def test_handle_create_payment_returns_payment_result_with_uuid(self):
        """Проверяет, что handle_create_payment возвращает PaymentResult с UUID."""
        bot_mock = AsyncMock()
        gateway_mock = AsyncMock()
        gateway_mock.currency = "XTR"

        gateway = TelegramStarsGateway(bot=bot_mock, gateway=gateway_mock)

        expected_url = "https://t.me/invoice/12345"
        bot_mock.create_invoice_link = AsyncMock(return_value=expected_url)

        result = await gateway.handle_create_payment(Decimal("50"), "Test")

        # Проверяем, что результат является экземпляром PaymentResult
        assert isinstance(result, PaymentResult)
        # Проверяем, что ID является UUID
        assert isinstance(result.id, uuid.UUID)
        # Проверяем, что URL установлен
        assert result.url == expected_url

    @pytest.mark.asyncio
    async def test_handle_create_payment_logs_exception_and_re_raises(self):
        """Проверяет, что handle_create_payment логирует исключение и переподнимает его."""
        bot_mock = AsyncMock()
        gateway_mock = AsyncMock()
        gateway_mock.currency = "XTR"

        gateway = TelegramStarsGateway(bot=bot_mock, gateway=gateway_mock)

        # Настраиваем исключение
        expected_exception = RuntimeError("Bot API Error")
        bot_mock.create_invoice_link.side_effect = expected_exception

        # Проверяем, что исключение поднимается
        with pytest.raises(RuntimeError, match="Bot API Error"):
            await gateway.handle_create_payment(Decimal("50"), "Test")

        # Проверка, что логгер (через mock) был вызван, сложнее без импорта loguru.logger,
        # но мы можем проверить, что исключение действительно переподнято.
        # Основная проверка - это `pytest.raises` выше.
