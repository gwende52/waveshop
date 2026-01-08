import pytest
from unittest.mock import Mock, patch
from pydantic import ValidationError
from src.infrastructure.database.models.dto import BaseDto
from src.core.utils.adapter import DialogDataAdapter


class MockDto(BaseDto):
    """Мок DTO для тестирования."""

    id: int
    name: str


class TestDialogDataAdapter:
    """Поверхностные юнит-тесты для DialogDataAdapter."""

    def test_init_method_exists(self):
        """Проверяет, что метод __init__ существует."""
        assert callable(getattr(DialogDataAdapter, "__init__", None))

    def test_load_method_exists(self):
        """Проверяет, что метод load существует."""
        assert callable(getattr(DialogDataAdapter, "load", None))

    def test_save_method_exists(self):
        """Проверяет, что метод save существует."""
        assert callable(getattr(DialogDataAdapter, "save", None))

    def test_init_creates_instance(self):
        """Проверяет, что __init__ создает экземпляр с dialog_manager."""
        mock_dialog_manager = Mock()
        adapter = DialogDataAdapter(dialog_manager=mock_dialog_manager)
        assert adapter.dialog_manager is mock_dialog_manager

    def test_load_returns_none_if_no_data(self):
        """Проверяет, что load возвращает None, если данных нет."""
        mock_dialog_manager = Mock()
        mock_dialog_manager.dialog_data = {}
        adapter = DialogDataAdapter(dialog_manager=mock_dialog_manager)

        result = adapter.load(MockDto)
        assert result is None

    def test_save_method_calls_dialog_manager(self):
        """Проверяет, что save записывает данные в dialog_manager."""
        mock_dialog_manager = Mock()
        mock_dialog_manager.dialog_data = {}
        adapter = DialogDataAdapter(dialog_manager=mock_dialog_manager)

        test_model = MockDto(id=1, name="test")
        expected_key = "mockdto"
        expected_data = {"id": 1, "name": "test"}

        result = adapter.save(test_model)

        assert mock_dialog_manager.dialog_data[expected_key] == expected_data
        assert result == expected_data

    def test_load_calls_model_validate(self):
        """Проверяет, что load вызывает model_validate на классе модели."""
        mock_dialog_manager = Mock()
        test_data = {"id": 1, "name": "test"}
        mock_dialog_manager.dialog_data = {"mockdto": test_data}
        adapter = DialogDataAdapter(dialog_manager=mock_dialog_manager)

        # Мокаем model_validate
        with patch.object(MockDto, "model_validate") as mock_validate:
            mock_validate.return_value = MockDto(id=1, name="test")

            result = adapter.load(MockDto)

            mock_validate.assert_called_once_with(test_data)
            assert result is not None

    def test_load_returns_none_on_validation_error(self):
        """Проверяет, что load возвращает None при ValidationError."""
        mock_dialog_manager = Mock()
        test_data = {"id": "invalid_type", "name": "test"}  # id должен быть int
        mock_dialog_manager.dialog_data = {"mockdto": test_data}
        adapter = DialogDataAdapter(dialog_manager=mock_dialog_manager)

        result = adapter.load(MockDto)
        assert result is None

    def test_save_handles_exception_gracefully(self):
        """Проверяет, что save не падает при исключении."""
        mock_dialog_manager = Mock()

        # Вызываем исключение при попытке записи
        def raise_error(key, value):
            raise RuntimeError("Write error")

        mock_dialog_manager.dialog_data.__setitem__ = Mock(side_effect=raise_error)
        adapter = DialogDataAdapter(dialog_manager=mock_dialog_manager)

        test_model = MockDto(id=1, name="test")

        # Это не должно вызвать исключение
        result = adapter.save(test_model)
        # Но результат data должен вернуться
        assert result == {"id": 1, "name": "test"}
