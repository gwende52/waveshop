import pytest
from unittest.mock import Mock
from src.bot.filters import SuperDevFilter


@pytest.mark.asyncio
async def test_super_dev_filter_match():
    filter_instance = SuperDevFilter()

    config = Mock()
    config.bot.dev_id = 123456

    user = Mock()
    user.telegram_id = 123456

    data = {"config": config, "user": user}

    result = await filter_instance.__call__(Mock(), **data)
    assert result is True


@pytest.mark.asyncio
async def test_super_dev_filter_no_match():
    filter_instance = SuperDevFilter()

    config = Mock()
    config.bot.dev_id = 123456

    user = Mock()
    user.telegram_id = 999999

    data = {"config": config, "user": user}

    result = await filter_instance.__call__(Mock(), **data)
    assert result is False


@pytest.mark.asyncio
async def test_super_dev_filter_no_user_key():
    filter_instance = SuperDevFilter()

    config = Mock()
    config.bot.dev_id = 123456

    data = {"config": config}  # Нет ключа user

    # Ожидаем KeyError, так как в коде явно используется data[USER_KEY]
    with pytest.raises(KeyError):
        await filter_instance.__call__(Mock(), **data)


@pytest.mark.asyncio
async def test_super_dev_filter_no_config_key():
    filter_instance = SuperDevFilter()

    user = Mock()
    user.telegram_id = 123456

    data = {"user": user}  # Нет ключа config

    # Ожидаем KeyError, так как в коде явно используется data[CONFIG_KEY]
    with pytest.raises(KeyError):
        await filter_instance.__call__(Mock(), **data)
