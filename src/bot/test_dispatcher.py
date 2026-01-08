from unittest.mock import Mock
from src.bot.dispatcher import create_dispatcher, create_bg_manager_factory
from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage


def test_create_dispatcher_returns_dispatcher():
    config = Mock()
    config.redis.dsn = "redis://localhost:6379/0"
    config.bot = Mock()

    dp = create_dispatcher(config)

    assert isinstance(dp, Dispatcher)


def test_create_dispatcher_storage_is_redis():
    config = Mock()
    config.redis.dsn = "redis://localhost:6379/0"
    config.bot = Mock()

    dp = create_dispatcher(config)

    assert isinstance(dp.storage, RedisStorage)


def test_create_bg_manager_factory():
    dp = Dispatcher()
    factory = create_bg_manager_factory(dp)

    # Проверим, что возвращается объект с нужным интерфейсом
    assert factory is not None


def test_dispatcher_config_is_set():
    config = Mock()
    config.redis.dsn = "redis://localhost:6379/0"
    config.bot = Mock()

    dp = create_dispatcher(config)

    # Проверим, что config передается в workflow_data
    assert dp.workflow_data.get("config") is config
