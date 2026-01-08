import pytest
from unittest.mock import Mock
from aiogram.enums import ChatType
from src.bot.filters import PrivateFilter


@pytest.mark.asyncio
async def test_private_filter_returns_bool():
    filter_instance = PrivateFilter()
    message = Mock()
    message.chat.type = ChatType.PRIVATE

    result = await filter_instance.__call__(message)
    assert result is True


@pytest.mark.asyncio
async def test_private_filter_group_chat():
    filter_instance = PrivateFilter()
    message = Mock()
    message.chat.type = ChatType.GROUP

    result = await filter_instance.__call__(message)
    assert result is False


@pytest.mark.asyncio
async def test_private_filter_supergroup():
    filter_instance = PrivateFilter()
    message = Mock()
    message.chat.type = ChatType.SUPERGROUP

    result = await filter_instance.__call__(message)
    assert result is False


@pytest.mark.asyncio
async def test_private_filter_channel():
    filter_instance = PrivateFilter()
    message = Mock()
    message.chat.type = ChatType.CHANNEL

    result = await filter_instance.__call__(message)
    assert result is False
