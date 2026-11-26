from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, Message

from bot.handlers.help import help_text
from bot.handlers.history import show_history_menu
from bot.handlers.settings import provider_menu
from bot.menus import back_menu, language_menu, main_menu, welcome_text
from bot.utils.checks import is_sudo
from bot.utils.storage import get_user, translate
from database import User
from telegram import filters, unpack


def start_command(bot: AsyncTeleBot) -> None:
    @bot.message_handler(commands=["start"], func=filters.private)
    async def _(message: Message) -> None:
        existing = await User.get(id=message.from_user.id)
        user = await get_user(message.from_user)
        t = translate(user)

        name = user.display_name
        if is_sudo(user.id):
            name = f"{name} ({t('start.admin')})"

        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        await bot.reply_to(
            message,
            welcome_text(t, name, existing is not None),
            reply_markup=main_menu(t),
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("menu:"))
    async def _(call: CallbackQuery) -> None:
        if call.message is None:
            await bot.answer_callback_query(call.id)
            return

        user = await get_user(call.from_user)
        t = translate(user)
        action = unpack(call.data)[1]
        chat_id = call.message.chat.id
        message_id = call.message.message_id

        if action == "back":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=welcome_text(t, user.display_name, True),
                reply_markup=main_menu(t),
            )
        elif action == "settings":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=t("settings.title"),
                reply_markup=await provider_menu(user, t),
            )
        elif action == "history":
            await show_history_menu(bot, user, t, chat_id, message_id)
        elif action == "language":
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=t("language.title"),
                reply_markup=language_menu(t),
            )
        elif action == "help":
            me = await bot.get_me()
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=help_text(t, me.username),
                reply_markup=back_menu(t),
            )
        else:
            hints = {
                "chat": t("start.chat_hint"),
                "image": t("start.image_hint"),
                "voice": t("start.voice_hint"),
            }
            await bot.answer_callback_query(call.id, hints.get(action, t("errors.unknown")), show_alert=True)
