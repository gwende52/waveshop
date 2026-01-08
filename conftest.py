# conftest.py
import sys
import base64
from pathlib import Path
from pydantic import SecretStr

# 🚨 Генерируем ЧЁТКО 32-байтовый ключ
_VALID_FERNET_KEY_BYTES = b"0123456789abcdef0123456789abcdef"
_VALID_FERNET_KEY_B64 = base64.urlsafe_b64encode(_VALID_FERNET_KEY_BYTES).decode()

assert len(_VALID_FERNET_KEY_BYTES) == 32
assert len(_VALID_FERNET_KEY_B64) == 44


# === ВЛОЖЕННЫЕ КОНФИГИ (без MagicMock) ===


class _FakeBotConfig:
    token = "123456:TEST"
    secret_token = "test_secret"
    dev_id = 123456789
    support_username = "test_support"
    mini_app_url = ""
    reset_webhook = False
    drop_pending_updates = False
    setup_commands = False
    use_banners = False


class _FakeRemnawaveConfig:
    host = "localhost"
    token = "test_remnawave_token"
    webhook_secret = "test_webhook_secret"
    caddy_token = ""
    cookie = ""


class _FakeDatabaseConfig:
    # Для совместимости — хотя в unit-тестах не используется
    host = "localhost"
    port = 5432
    name = "test_db"
    user = "test"
    password = "test"
    echo = False
    echo_pool = False
    pool_size = 5
    max_overflow = 10
    pool_timeout = 5
    pool_recycle = 3600

    # Если где-то используется dsn — добавим
    @property
    def dsn(self):
        return "sqlite+aiosqlite:///:memory:"


class _FakeRedisConfig:
    dsn = "redis://localhost:6379/15"


class _FakeAppConfig:
    def __init__(self):
        # Обязательные SecretStr
        self.crypt_key = SecretStr(_VALID_FERNET_KEY_B64)
        self.domain = SecretStr("localhost")

        # Простые поля
        self.host = "127.0.0.1"
        self.port = 5000
        self.locales = ["en"]
        self.default_locale = "en"
        self.assets_dir = Path(__file__).parent / "assets"
        self.origins = []

        # Вложенные конфиги — ЧИСТЫЕ ОБЪЕКТЫ
        self.bot = _FakeBotConfig()
        self.remnawave = _FakeRemnawaveConfig()
        self.database = _FakeDatabaseConfig()
        self.redis = _FakeRedisConfig()

    @property
    def banners_dir(self) -> Path:
        return self.assets_dir / "banners"

    @property
    def translations_dir(self) -> Path:
        return self.assets_dir / "translations"

    def get_webhook(self, gateway_type):
        return f"https://localhost/webhook/{gateway_type}"


def _fake_get():
    return _FakeAppConfig()


# 🔑 Подменяем ДО импорта crypto
import src.core.config.app

src.core.config.app.AppConfig.get = staticmethod(_fake_get)


# 🔐 Мокаем crypto-модуль, чтобы избежать повторного вызова Fernet
try:
    import src.core.security.crypto as crypto_mod

    fake = _FakeAppConfig()
    fake_key = fake.crypt_key.get_secret_value().encode()
    from cryptography.fernet import Fernet

    crypto_mod._cipher_suite = Fernet(fake_key)
    crypto_mod.encrypt = lambda s: f"enc({s})"
    crypto_mod.decrypt = lambda s: s.removeprefix("enc(").removesuffix(")")
    crypto_mod.deep_decrypt = lambda x: x
except Exception:
    pass


import pytest


def pytest_configure(config):
    print("✅ AppConfig fully mocked (no MagicMock)")


@pytest.fixture(autouse=True)
def _ensure_assets():
    Path("assets/banners").mkdir(parents=True, exist_ok=True)
    Path("assets/translations").mkdir(parents=True, exist_ok=True)
