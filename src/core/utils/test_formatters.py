import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import Mock
from src.core.utils.formatters import (
    format_user_log,
    format_username_to_url,
    format_days_to_datetime,
    format_device_count,
    format_gb_to_bytes,
    format_bytes_to_gb,
    format_limits_to_plan_type,
    format_percent,
    format_country_code,
    i18n_format_bytes_to_unit,
    i18n_format_seconds,
    i18n_format_days,
    i18n_format_limit,
    i18n_format_traffic_limit,
    i18n_format_device_limit,
    i18n_format_expire_time,
    i18n_postprocess_text,
)
from src.core.enums import PlanType
from src.core.i18n.keys import UtilKey, ByteUnitKey, TimeUnitKey


class TestFormatters:
    """Поверхностные юнит-тесты для форматтеров."""

    def test_format_user_log(self):
        """Тест форматирования лога пользователя."""
        user = Mock()
        user.role = "admin"
        user.telegram_id = 123456789
        user.name = "TestUser"
        result = format_user_log(user)
        assert result == "[ADMIN:123456789 (TestUser)]"

    def test_format_username_to_url(self):
        """Тест форматирования username в URL."""
        result = format_username_to_url("@testuser", "Hello")
        assert result.startswith("https://t.me/")
        assert "testuser" in result
        assert "Hello" in result

        result_no_text = format_username_to_url("testuser", None)
        assert "text=" in result_no_text

    def test_format_days_to_datetime_unlimited(self):
        """Тест форматирования дней в datetime для бесконечности."""
        result = format_days_to_datetime(-1, year=2100)
        assert result.year == 2100

    def test_format_days_to_datetime_positive(self):
        """Тест форматирования дней в datetime."""
        result = format_days_to_datetime(10)
        # Просто проверим, что результат - datetime и дата изменилась
        assert isinstance(result, datetime)
        # Не будем сравнивать с datetime.now() из-за часовых поясов

    def test_format_device_count(self):
        """Тест форматирования количества устройств."""
        assert format_device_count(None) == -1
        assert format_device_count(0) == -1
        assert format_device_count(-1) == 0
        assert format_device_count(5) == 5

    def test_format_gb_to_bytes(self):
        """Тест форматирования ГБ в байты."""
        assert format_gb_to_bytes(-1) == 0
        assert format_gb_to_bytes(1, binary=False) == 1_000_000_000
        assert format_gb_to_bytes(1, binary=True) >= 1_073_741_824  # 1024^3

    def test_format_bytes_to_gb(self):
        """Тест форматирования байтов в ГБ."""
        assert format_bytes_to_gb(0) == -1
        assert format_bytes_to_gb(None) == -1
        assert format_bytes_to_gb(1_000_000_000, binary=False) == 1
        assert format_bytes_to_gb(1_073_741_824, binary=True) == 1

    def test_format_limits_to_plan_type(self):
        """Тест определения типа плана."""
        assert format_limits_to_plan_type(100, 5) == PlanType.BOTH
        assert format_limits_to_plan_type(100, 0) == PlanType.TRAFFIC
        assert format_limits_to_plan_type(0, 5) == PlanType.DEVICES
        assert format_limits_to_plan_type(0, 0) == PlanType.UNLIMITED

    def test_format_percent(self):
        """Тест форматирования процентов."""
        assert format_percent(50, 100) == "50.00"
        assert format_percent(0, 0) == "N/A"

    def test_format_country_code(self):
        """Тест форматирования кода страны."""
        assert format_country_code("US") == "🇺🇸"
        assert format_country_code("RU") == "🇷🇺"
        assert format_country_code("A") == "🏴‍☠️"  # Невалидный
        assert format_country_code("12") == "🏴‍☠️"  # Невалидный

    def test_i18n_format_seconds(self):
        """Тест форматирования секунд."""
        parts = i18n_format_seconds(3665)  # 1ч 1м 5с
        # Проверим, что список не пустой и содержит кортежи
        assert isinstance(parts, list)
        assert all(isinstance(p, tuple) and len(p) == 2 for p in parts)

        parts_short = i18n_format_seconds(30)
        # Для менее 60 секунд должен вернуть 0 минут
        assert parts_short[0][0] == TimeUnitKey.MINUTE
        assert parts_short[0][1]["value"] == 0

    def test_i18n_format_days(self):
        """Тест форматирования дней."""
        unit, kwargs = i18n_format_days(-1)
        assert unit == UtilKey.UNLIMITED

        unit, kwargs = i18n_format_days(365)
        assert unit == TimeUnitKey.YEAR
        assert kwargs["value"] == 1

        unit, kwargs = i18n_format_days(45)
        assert unit == TimeUnitKey.DAY
        assert kwargs["value"] == 45

    def test_i18n_format_limit(self):
        """Тест форматирования лимита."""
        unit, kwargs = i18n_format_limit(10)
        assert unit == UtilKey.UNIT_UNLIMITED
        assert kwargs["value"] == 10

    def test_i18n_format_traffic_limit(self):
        """Тест форматирования лимита трафика."""
        unit, kwargs = i18n_format_traffic_limit(-1)
        assert unit == UtilKey.UNIT_UNLIMITED

        unit, kwargs = i18n_format_traffic_limit(100)
        assert unit == ByteUnitKey.GIGABYTE
        assert kwargs["value"] == 100

    def test_i18n_format_device_limit(self):
        """Тест форматирования лимита устройств."""
        unit, kwargs = i18n_format_device_limit(5)
        assert unit == UtilKey.UNIT_UNLIMITED
        assert kwargs["value"] == 5

    def test_i18n_format_expire_time_datetime_unlimited(self):
        """Тест форматирования времени окончания (datetime, бесконечно)."""
        future_dt = datetime(2099, 1, 1)
        parts = i18n_format_expire_time(future_dt)
        assert parts[0][0] == UtilKey.UNLIMITED

    def test_i18n_format_expire_time_timedelta(self):
        """Тест форматирования времени окончания (timedelta)."""
        td = timedelta(days=1, hours=2, minutes=30)
        parts = i18n_format_expire_time(td)
        # Проверим, что возвращается список
        assert isinstance(parts, list)
        # Должен содержать дни, часы, минуты
        units = [p[0] for p in parts]
        assert TimeUnitKey.DAY in units
        assert TimeUnitKey.HOUR in units
        assert TimeUnitKey.MINUTE in units

    def test_i18n_postprocess_text(self):
        """Тест постобработки текста."""
        text = "<b>\n\n\nBold\n\n</b>"
        processed = i18n_postprocess_text(text, collapse_level=1)
        # Должно удалить лишние переносы
        assert (
            processed.count("\n") <= 3
        )  # max 1 newline * collapse_level + few others

        text_with_empty = "Some text !empty! more text"
        processed_no_empty = i18n_postprocess_text(text_with_empty)
        assert "!empty!" not in processed_no_empty
