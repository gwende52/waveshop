from src.bot.keyboards import (
    get_renew_keyboard,
    get_channel_keyboard,
    get_rules_keyboard,
    get_contact_support_keyboard,
    get_waveshop_keyboard,
    get_waveshop_update_keyboard,
    get_user_keyboard,
    CALLBACK_CHANNEL_CONFIRM,
    CALLBACK_RULES_ACCEPT,
)


def test_get_renew_keyboard():
    keyboard = get_renew_keyboard()
    assert keyboard is not None
    # Проверим, что клавиатура содержит кнопки
    assert hasattr(keyboard, "inline_keyboard")


def test_get_channel_keyboard():
    keyboard = get_channel_keyboard("https://t.me/channel")
    assert keyboard is not None
    # Проверим, что первая кнопка - это join
    first_row = keyboard.inline_keyboard[0]
    assert first_row[0].text == "btn-channel-join"
    # Проверим, что вторая кнопка - это confirm
    second_row = keyboard.inline_keyboard[1]
    assert second_row[0].text == "btn-channel-confirm"
    assert second_row[0].callback_data == CALLBACK_CHANNEL_CONFIRM


def test_get_rules_keyboard():
    keyboard = get_rules_keyboard()
    assert keyboard is not None
    first_row = keyboard.inline_keyboard[0]
    assert first_row[0].text == "btn-rules-accept"
    assert first_row[0].callback_data == CALLBACK_RULES_ACCEPT


def test_get_contact_support_keyboard():
    keyboard = get_contact_support_keyboard("username", "text")
    assert keyboard is not None
    first_row = keyboard.inline_keyboard[0]
    assert first_row[0].text == "btn-contact-support"


def test_get_waveshop_keyboard():
    keyboard = get_waveshop_keyboard()
    assert keyboard is not None
    # Проверим, что есть кнопки в первой строке
    first_row = keyboard.inline_keyboard[0]
    assert len(first_row) == 3


def test_get_waveshop_update_keyboard():
    keyboard = get_waveshop_update_keyboard()
    assert keyboard is not None
    # Проверим, что есть две кнопки в строке
    first_row = keyboard.inline_keyboard[0]
    assert len(first_row) == 2


def test_get_user_keyboard():
    keyboard = get_user_keyboard(123456)
    assert keyboard is not None
    first_row = keyboard.inline_keyboard[0]
    assert first_row[0].text == "btn-goto-user-profile"
    # Проверим, что в callback_data содержится префикс и id
    assert "123456" in first_row[0].callback_data
