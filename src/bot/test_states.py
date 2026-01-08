from src.bot.states import MainMenu, Subscription, state_from_string
from aiogram.fsm.state import State


def test_main_menu_states():
    assert isinstance(MainMenu.MAIN, State)
    assert isinstance(MainMenu.DEVICES, State)
    assert isinstance(MainMenu.INVITE, State)
    assert isinstance(MainMenu.INVITED_USERS, State)


def test_subscription_states():
    assert isinstance(Subscription.MAIN, State)
    assert isinstance(Subscription.PROMOCODE, State)
    assert isinstance(Subscription.PLANS, State)
    assert isinstance(Subscription.DURATION, State)
    assert isinstance(Subscription.PAYMENT_METHOD, State)
    assert isinstance(Subscription.CONFIRM, State)
    assert isinstance(Subscription.SUCCESS, State)
    assert isinstance(Subscription.FAILED, State)
    assert isinstance(Subscription.TRIAL, State)


def test_state_from_string_valid():
    state = state_from_string("MainMenu:MAIN")
    assert state == MainMenu.MAIN

    state = state_from_string("Subscription:PLANS")
    assert state == Subscription.PLANS


def test_state_from_string_invalid():
    state = state_from_string("NonExistent:STATE")
    assert state is None

    state = state_from_string("MainMenu:NONEXISTENT")
    assert state is None

    state = state_from_string("InvalidFormat")
    assert state is None

    state = state_from_string("")
    assert state is None


def test_state_from_string_custom_separator():
    # Тестируем с нестандартным разделителем
    # Хотя функция по умолчанию использует ':', проверим формат
    state = state_from_string("MainMenu:OTHER")
    assert state is not MainMenu.MAIN
