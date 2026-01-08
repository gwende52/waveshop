import asyncio
import secrets
import pytest

# Импорт из правильного модуля
from src.api.endpoints import TelegramWebhookEndpoint


class TestTelegramWebhookEndpoint:
    """Поверхностные юнит-тесты для TelegramWebhookEndpoint."""

    def test_verify_secret_with_matching_tokens(self):
        """Проверяет, что _verify_secret возвращает True для совпадающих токенов."""
        token = "test_secret_123"
        endpoint = TelegramWebhookEndpoint(dispatcher=None, secret_token=token)
        result = endpoint._verify_secret(token)
        assert result is True

    def test_verify_secret_with_different_tokens(self):
        """Проверяет, что _verify_secret возвращает False для разных токенов."""
        endpoint = TelegramWebhookEndpoint(dispatcher=None, secret_token="secret1")
        result = endpoint._verify_secret("secret2")
        assert result is False

    def test_verify_secret_with_empty_tokens(self):
        """Проверяет, что _verify_secret работает с пустыми токенами."""
        endpoint = TelegramWebhookEndpoint(dispatcher=None, secret_token="")
        result = endpoint._verify_secret("")
        # compare_digest должен вернуть True для двух пустых строк
        assert result is True

    def test_verify_secret_with_one_empty_token(self):
        """Проверяет, что _verify_secret возвращает False если один токен пустой."""
        endpoint = TelegramWebhookEndpoint(dispatcher=None, secret_token="non_empty")
        result = endpoint._verify_secret("")
        assert result is False
        result2 = endpoint._verify_secret("non_empty")
        assert result2 is True

    def test_initial_feed_update_tasks_set_is_empty(self):
        """Проверяет, что множество задач инициализируется пустым."""
        endpoint = TelegramWebhookEndpoint(dispatcher=None, secret_token="test")
        assert len(endpoint._feed_update_tasks) == 0

    def test_startup_method_exists(self):
        """Проверяет, что метод startup существует."""
        endpoint = TelegramWebhookEndpoint(dispatcher=None, secret_token="test")
        assert callable(getattr(endpoint, "startup", None))

    def test_shutdown_method_exists(self):
        """Проверяет, что метод shutdown существует."""
        endpoint = TelegramWebhookEndpoint(dispatcher=None, secret_token="test")
        assert callable(getattr(endpoint, "shutdown", None))

    def test_register_method_exists(self):
        """Проверяет, что метод register существует."""
        endpoint = TelegramWebhookEndpoint(dispatcher=None, secret_token="test")
        assert callable(getattr(endpoint, "register", None))

    def test_feed_update_method_exists(self):
        """Проверяет, что метод _feed_update существует."""
        endpoint = TelegramWebhookEndpoint(dispatcher=None, secret_token="test")
        assert callable(getattr(endpoint, "_feed_update", None))
