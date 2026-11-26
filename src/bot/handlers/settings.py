from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, Message

from bot.utils.storage import get_user, translate
from database import ProviderSetting, User
from providers import manager
from telegram import inline, pack, unpack


async def provider_menu(user: User, t) -> object:
    rows = []
    for name in manager.names():
        provider = manager.get(name)
        setting = await ProviderSetting.get(user_id=user.id, provider=name)
        enabled = bool(setting and setting.enabled)
        mark = "✅" if enabled else "❌"
        rows.append(
            [
                (
                    f"{mark} {provider.label}",
                    pack("settings", name),
                    "success" if enabled else "danger",
                )
            ]
        )
    rows.append([(t("common.back"), pack("menu", "back"), "primary")])
    rows.append([(t("common.close"), pack("settings", "close"), "primary")])
    return inline(rows)


def settings_command(bot: AsyncTeleBot) -> None:
    @bot.message_handler(commands=["settings"])
    async def _(message: Message) -> None:
        user = await get_user(message.from_user)
        t = translate(user)
        await bot.reply_to(
            message,
            t("settings.title"),
            reply_markup=await provider_menu(user, t),
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("settings:"))
    async def _(call: CallbackQuery) -> None:
        user = await get_user(call.from_user)
        t = translate(user)
        _, provider = unpack(call.data)

        if provider == "close":
            await bot.edit_message_text(
                t("settings.closed"),
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
            await bot.answer_callback_query(call.id)
            return

        if manager.get(provider) is None:
            await bot.answer_callback_query(call.id, t("errors.unknown"), show_alert=True)
            return

        enabled = await ProviderSetting.toggle(user.id, provider)
        status = t("settings.enabled" if enabled else "settings.disabled")
        await bot.answer_callback_query(
            call.id,
            t("settings.changed", provider=provider, status=status),
        )
        await bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=await provider_menu(user, t),
        )
