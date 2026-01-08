from uuid import UUID

from aiogram_dialog import Dialog, StartMode, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Column,
    CopyText,
    ListGroup,
    Row,
    Select,
    Start,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Format
from magic_filter import F

from src.bot.keyboards import main_menu_button
from src.bot.states import DashboardWaveshop, WaveshopPlans
from src.bot.widgets import Banner, I18nFormat, IgnoreUpdate
from src.core.enums import BannerName, Currency, PlanAvailability, PlanType

from .getters import (
    allowed_users_getter,
    availability_getter,
    configurator_getter,
    durations_getter,
    plans_getter,
    price_getter,
    prices_getter,
    squads_getter,
    type_getter,
)
from .handlers import (
    on_active_toggle,
    on_allowed_user_input,
    on_allowed_user_remove,
    on_availability_select,
    on_confirm_plan,
    on_currency_select,
    on_devices_input,
    on_duration_input,
    on_duration_remove,
    on_duration_select,
    on_name_input,
    on_plan_remove,
    on_plan_select,
    on_price_input,
    on_squad_select,
    on_squads,
    on_traffic_input,
    on_type_select,
)

plans = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-plans-main"),
    Row(
        SwitchTo(
            I18nFormat("btn-plans-create"),
            id="create",
            state=WaveshopPlans.CONFIGURATOR,
        ),
    ),
    ListGroup(
        Row(
            Button(
                text=I18nFormat(
                    "btn-plan",
                    name=F["item"]["name"],
                    is_active=F["item"]["is_active"],
                ),
                id="select_plan",
                on_click=on_plan_select,
            ),
            Button(
                text=Format("❌"),
                id="remove_plan",
                on_click=on_plan_remove,
            ),
        ),
        id="plans_list",
        item_id_getter=lambda item: item["id"],
        items="plans",
    ),
    Row(
        Start(
            text=I18nFormat("btn-back"),
            id="back",
            state=DashboardWaveshop.MAIN,
            mode=StartMode.RESET_STACK,
        ),
        *main_menu_button,
    ),
    IgnoreUpdate(),
    state=WaveshopPlans.MAIN,
    getter=plans_getter,
)

configurator = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-plan-configurator"),
    Row(
        SwitchTo(
            text=I18nFormat("btn-plan-name"),
            id="name",
            state=WaveshopPlans.NAME,
        ),
        SwitchTo(
            text=I18nFormat("btn-plan-type"),
            id="type",
            state=WaveshopPlans.TYPE,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-plan-availability"),
            id="availability",
            state=WaveshopPlans.AVAILABILITY,
        ),
        Button(
            text=I18nFormat("btn-plan-active", is_active=F["is_active"]),
            id="active_toggle",
            on_click=on_active_toggle,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-plan-traffic"),
            id="traffic",
            state=WaveshopPlans.TRAFFIC,
            when=~F["is_unlimited_traffic"],
        ),
        SwitchTo(
            text=I18nFormat("btn-plan-devices"),
            id="devices",
            state=WaveshopPlans.DEVICES,
            when=~F["is_unlimited_devices"],
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-plan-durations-prices"),
            id="durations_prices",
            state=WaveshopPlans.DURATIONS,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-plan-allowed"),
            id="allowed",
            state=WaveshopPlans.ALLOWED,
            when=F["availability"] == PlanAvailability.ALLOWED,
        ),
    ),
    Row(
        Button(
            text=I18nFormat("btn-plan-squads"),
            id="squads",
            on_click=on_squads,
        ),
    ),
    Row(
        Button(
            text=I18nFormat("btn-plan-confirm"),
            id="confirm",
            on_click=on_confirm_plan,
        ),
    ),
    Row(
        Start(
            text=I18nFormat("btn-back"),
            id="back",
            state=WaveshopPlans.MAIN,
            mode=StartMode.RESET_STACK,
        ),
    ),
    IgnoreUpdate(),
    state=WaveshopPlans.CONFIGURATOR,
    getter=configurator_getter,
)

plan_name = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-plan-name"),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=WaveshopPlans.CONFIGURATOR,
        ),
    ),
    MessageInput(func=on_name_input),
    IgnoreUpdate(),
    state=WaveshopPlans.NAME,
)

plan_type = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-plan-type"),
    Column(
        Select(
            text=I18nFormat("btn-plan-type-choice", type=F["item"]),
            id="select_type",
            item_id_getter=lambda item: item.value,
            items="types",
            type_factory=PlanType,
            on_click=on_type_select,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=WaveshopPlans.CONFIGURATOR,
        ),
    ),
    IgnoreUpdate(),
    state=WaveshopPlans.TYPE,
    getter=type_getter,
)

plan_availability = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-plan-availability"),
    Column(
        Select(
            text=I18nFormat("btn-plan-availability-choice", type=F["item"]),
            id="select_availability",
            item_id_getter=lambda item: item.value,
            items="availability",
            type_factory=PlanAvailability,
            on_click=on_availability_select,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=WaveshopPlans.CONFIGURATOR,
        ),
    ),
    IgnoreUpdate(),
    state=WaveshopPlans.AVAILABILITY,
    getter=availability_getter,
)

plan_traffic = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-plan-traffic"),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=WaveshopPlans.CONFIGURATOR,
        ),
    ),
    MessageInput(func=on_traffic_input),
    IgnoreUpdate(),
    state=WaveshopPlans.TRAFFIC,
)

plan_devices = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-plan-devices"),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=WaveshopPlans.CONFIGURATOR,
        ),
    ),
    MessageInput(func=on_devices_input),
    IgnoreUpdate(),
    state=WaveshopPlans.DEVICES,
)


plan_durations = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-plan-durations"),
    ListGroup(
        Row(
            Button(
                text=I18nFormat("btn-plan-duration", value=F["item"]["days"]),
                id="select_duration",
                on_click=on_duration_select,  # type: ignore[arg-type]
            ),
            Button(
                text=Format("❌"),
                id="remove_duration",
                on_click=on_duration_remove,
                when=F["data"]["deletable"],
            ),
        ),
        id="duration_list",
        item_id_getter=lambda item: item["days"],
        items="durations",
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-plan-duration-add"),
            id="duration_add",
            state=WaveshopPlans.DURATION_ADD,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=WaveshopPlans.CONFIGURATOR,
        ),
    ),
    IgnoreUpdate(),
    state=WaveshopPlans.DURATIONS,
    getter=durations_getter,
)

plan_durations_add = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-plan-duration"),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=WaveshopPlans.DURATIONS,
        ),
    ),
    MessageInput(func=on_duration_input),
    IgnoreUpdate(),
    state=WaveshopPlans.DURATION_ADD,
)

plan_prices = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-plan-prices", value=F["duration"]),
    Column(
        Select(
            text=I18nFormat(
                "btn-plan-price-choice",
                price=F["item"]["price"],
                currency=F["item"]["currency"].value,
            ),
            id="select_price",
            item_id_getter=lambda item: item["currency"].value,
            items="prices",
            type_factory=Currency,
            on_click=on_currency_select,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=WaveshopPlans.DURATIONS,
        ),
    ),
    IgnoreUpdate(),
    state=WaveshopPlans.PRICES,
    getter=prices_getter,
)

plan_price = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-plan-price", value=F["duration"], currency=F["currency"]),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=WaveshopPlans.PRICES,
        ),
    ),
    MessageInput(func=on_price_input),
    IgnoreUpdate(),
    state=WaveshopPlans.PRICE,
    getter=price_getter,
)

plan_allowed_users = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-plan-allowed-users"),
    ListGroup(
        Row(
            CopyText(
                text=Format("{item}"),
                copy_text=Format("{item}"),
            ),
            Button(
                text=Format("❌"),
                id="remove_allowed_user",
                on_click=on_allowed_user_remove,
            ),
        ),
        id="allowed_users_list",
        item_id_getter=lambda item: item,
        items="allowed_users",
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=WaveshopPlans.CONFIGURATOR,
        ),
    ),
    MessageInput(func=on_allowed_user_input),
    IgnoreUpdate(),
    state=WaveshopPlans.ALLOWED,
    getter=allowed_users_getter,
)

plan_squads = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-plan-squads"),
    Column(
        Select(
            text=I18nFormat(
                "btn-squad-choice",
                name=F["item"]["name"],
                selected=F["item"]["selected"],
            ),
            id="select_squad",
            item_id_getter=lambda item: item["uuid"],
            items="squads",
            type_factory=UUID,
            on_click=on_squad_select,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=WaveshopPlans.CONFIGURATOR,
        ),
    ),
    IgnoreUpdate(),
    state=WaveshopPlans.SQUADS,
    getter=squads_getter,
)

router = Dialog(
    plans,
    configurator,
    plan_name,
    plan_type,
    plan_availability,
    plan_traffic,
    plan_devices,
    plan_durations,
    plan_durations_add,
    plan_prices,
    plan_price,
    plan_allowed_users,
    plan_squads,
)
