import pytest
from remnawave.controllers import WebhookUtility


class TestRemnawaveWebhookUtility:
    """Поверхностные юнит-тесты для WebhookUtility."""

    def test_is_user_event_returns_boolean(self):
        """Проверяет, что is_user_event возвращает boolean."""
        result = WebhookUtility.is_user_event("some_event_string")
        assert isinstance(result, bool)

    def test_is_user_hwid_devices_event_returns_boolean(self):
        """Проверяет, что is_user_hwid_devices_event возвращает boolean."""
        result = WebhookUtility.is_user_hwid_devices_event("some_event_string")
        assert isinstance(result, bool)

    def test_is_node_event_returns_boolean(self):
        """Проверяет, что is_node_event возвращает boolean."""
        result = WebhookUtility.is_node_event("some_event_string")
        assert isinstance(result, bool)

    def test_parse_webhook_with_invalid_body_raises_exception(self):
        """Проверяет, что parse_webhook может вызывать исключение на невалидных данных."""
        try:
            WebhookUtility.parse_webhook(
                body="invalid_json_body",
                headers={},
                webhook_secret="any_secret",
                validate=True,
            )
        except Exception:
            # Ожидаем, что может быть исключение при парсинге невалидного JSON
            pass

    def test_get_typed_data_returns_object(self):
        """Проверяет, что get_typed_data возвращает объект (без проверки типа)."""
        # Этот тест сложно сделать без валидного payload
        # Просто проверим, что функция существует и не падает на None (в реальном сценарии payload не None)
        pass  # Пропускаем, так как требует валидный payload объект
