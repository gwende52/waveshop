from aiogram_dialog import Dialog, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, ListGroup, Row, Start, SwitchTo
from aiogram_dialog.widgets.text import Format
from magic_filter import F

from src.bot.keyboards import main_menu_button
from src.bot.routers.extra.test import show_dev_popup
from src.bot.states import (
    Dashboard,
    DashboardWaveshop,
    WaveshopGateways,
    WaveshopNotifications,
    WaveshopPlans,
)
from src.bot.widgets import Banner, I18nFormat, IgnoreUpdate
from src.core.enums import BannerName

from .getters import admins_getter
from .handlers import on_logs_request, on_user_role_remove, on_user_select

waveshop = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-waveshop-main"),
    Row(
        SwitchTo(
            text=I18nFormat("btn-waveshop-admins"),
            id="admins",
            state=DashboardWaveshop.ADMINS,
        ),
    ),
    Row(
        Start(
            text=I18nFormat("btn-waveshop-gateways"),
            id="gateways",
            state=WaveshopGateways.MAIN,
        ),
    ),
    Row(
        Button(
            text=I18nFormat("btn-waveshop-referral"),
            id="referral",
            # state=DashboardWaveshop.REFERRAL,
            on_click=show_dev_popup,
        ),
        Button(
            text=I18nFormat("btn-waveshop-advertising"),
            id="advertising",
            # state=DashboardWaveshop.ADVERTISING,
            on_click=show_dev_popup,
        ),
    ),
    Row(
        Start(
            text=I18nFormat("btn-waveshop-plans"),
            id="plans",
            state=WaveshopPlans.MAIN,
            mode=StartMode.RESET_STACK,
        ),
        Start(
            text=I18nFormat("btn-waveshop-notifications"),
            id="notifications",
            state=WaveshopNotifications.MAIN,
        ),
    ),
    Row(
        Button(
            text=I18nFormat("btn-waveshop-logs"),
            id="logs",
            on_click=on_logs_request,
        ),
        Button(
            text=I18nFormat("btn-waveshop-audit"),
            id="audit",
            on_click=show_dev_popup,
        ),
    ),
    Row(
        Start(
            text=I18nFormat("btn-back"),
            id="back",
            state=Dashboard.MAIN,
            mode=StartMode.RESET_STACK,
        ),
        *main_menu_button,
    ),
    IgnoreUpdate(),
    state=DashboardWaveshop.MAIN,
)

admins = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-admins-main"),
    ListGroup(
        Row(
            Button(
                text=Format("{item[user_id]} ({item[user_name]})"),
                id="select_user",
                on_click=on_user_select,
            ),
            Button(
                text=Format("❌"),
                id="remove_role",
                on_click=on_user_role_remove,
                when=F["item"]["deletable"],
            ),
        ),
        id="admins_list",
        item_id_getter=lambda item: item["user_id"],
        items="admins",
    ),
    Row(
        Start(
            text=I18nFormat("btn-back"),
            id="back",
            state=DashboardWaveshop.MAIN,
            mode=StartMode.RESET_STACK,
        ),
    ),
    IgnoreUpdate(),
    state=DashboardWaveshop.ADMINS,
    getter=admins_getter,
)

router = Dialog(
    waveshop,
    admins,
)
