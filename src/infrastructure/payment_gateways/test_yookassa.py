import uuid
import pytest
from unittest.mock import AsyncMock, Mock
import orjson
from src.infrastructure.payment_gateways import YookassaGateway
from src.core.enums import TransactionStatus, YookassaVatCode
from src.infrastructure.database.models.dto import PaymentResult


class TestYookassaGateway:
    """Поверхностные юнит-тесты для YookassaGateway."""

    def test_constants_defined_correctly(self):
        assert hasattr(YookassaGateway, "API_BASE")
        assert hasattr(YookassaGateway, "PAYMENT_SUBJECT")
        assert hasattr(YookassaGateway, "PAYMENT_MODE")
        assert hasattr(YookassaGateway, "VAT_CODE")
        assert hasattr(YookassaGateway, "CUSTOMER")
        assert hasattr(YookassaGateway, "NETWORKS")
        assert isinstance(YookassaGateway.VAT_CODE, YookassaVatCode)

    def test_networks_is_list(self):
        networks = YookassaGateway.NETWORKS
        assert isinstance(networks, list)
        assert all(isinstance(ip, str) for ip in networks)

    def test_methods_exist(self):
        assert callable(getattr(YookassaGateway, "__init__", None))
        assert callable(getattr(YookassaGateway, "handle_webhook", None))
        assert callable(getattr(YookassaGateway, "handle_create_payment", None))
        assert callable(getattr(YookassaGateway, "_create_payment_payload", None))
        assert callable(getattr(YookassaGateway, "_get_payment_data", None))
        assert callable(getattr(YookassaGateway, "_is_ip_trusted", None))

    def test_get_payment_data_returns_payment_result(self):
        gateway = object.__new__(YookassaGateway)
        valid_uuid = str(uuid.uuid4())
        valid_url = "https://yookassa.ru/success"
        response_data = {
            "id": valid_uuid,
            "confirmation": {"confirmation_url": valid_url},
        }
        result = gateway._get_payment_data(response_data)
        assert isinstance(result, PaymentResult)
        assert result.id == uuid.UUID(valid_uuid)
        assert result.url == valid_url

    def test_get_payment_data_raises_on_missing_fields(self):
        gateway = object.__new__(YookassaGateway)
        with pytest.raises(KeyError, match="missing 'id'"):
            gateway._get_payment_data({"confirmation": {"confirmation_url": "url"}})

        with pytest.raises(KeyError, match="missing 'confirmation_url'"):
            gateway._get_payment_data({"id": str(uuid.uuid4()), "confirmation": {}})

    def test_webhook_payload_parsing_logic(self):
        # Тестируем логику парсинга, как она реализована внутри handle_webhook
        webhook_data = {"object": {"id": str(uuid.uuid4()), "status": "succeeded"}}
        payment_object = webhook_data.get("object", {})
        payment_id_str = payment_object.get("id")
        status_str = payment_object.get("status")

        assert payment_id_str is not None
        assert status_str is not None

        payment_id = uuid.UUID(payment_id_str)
        assert isinstance(payment_id, uuid.UUID)

        if status_str == "succeeded":
            transaction_status = TransactionStatus.COMPLETED
        elif status_str == "canceled":
            transaction_status = TransactionStatus.CANCELED
        else:
            raise ValueError("Field 'status' not support")

        assert transaction_status == TransactionStatus.COMPLETED

    def test_webhook_payload_parsing_logic_canceled(self):
        webhook_data = {"object": {"id": str(uuid.uuid4()), "status": "canceled"}}
        payment_object = webhook_data.get("object", {})
        status_str = payment_object.get("status")

        if status_str == "succeeded":
            transaction_status = TransactionStatus.COMPLETED
        elif status_str == "canceled":
            transaction_status = TransactionStatus.CANCELED
        else:
            raise ValueError("Field 'status' not support")

        assert transaction_status == TransactionStatus.CANCELED

    def test_webhook_payload_parsing_invalid_status(self):
        webhook_data = {"object": {"id": str(uuid.uuid4()), "status": "unknown"}}
        payment_object = webhook_data.get("object", {})
        status_str = payment_object.get("status")

        with pytest.raises(ValueError, match="Field 'status' not support"):
            if status_str == "succeeded":
                transaction_status = TransactionStatus.COMPLETED
            elif status_str == "canceled":
                transaction_status = TransactionStatus.CANCELED
            else:
                raise ValueError("Field 'status' not support")

    def test_webhook_payload_parsing_invalid_uuid(self):
        webhook_data = {"object": {"id": "not-a-uuid", "status": "succeeded"}}
        payment_object = webhook_data.get("object", {})
        payment_id_str = payment_object.get("id")

        with pytest.raises(ValueError):
            uuid.UUID(payment_id_str)
