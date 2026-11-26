from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, Message
from telebot.util import extract_arguments

from bot.menus import language_menu, main_menu, welcome_text
from bot.utils.storage import get_user, translate
from i18n import i18n
from telegram import unpack


def language_command(bot: AsyncTeleBot) -> None:
    @bot.message_handler(commands=["language"])
    async def _(message: Message) -> None:
        user = await get_user(message.from_user)
        t = translate(user)
        code = extract_arguments(message.text).strip().lower()

        if code:
            if code not in i18n.languages:
                await bot.reply_to(message, t("language.usage"))
                return
            user.language = code
            await user.save()
            await bot.reply_to(message, translate(user)("language.changed", lang=code.upper()))
            return

        await bot.reply_to(message, t("language.title"), reply_markup=language_menu(t))

    @bot.callback_query_handler(func=lambda call: call.data.startswith("lang:"))
    async def _(call: CallbackQuery) -> None:
        if call.message is None:
            await bot.answer_callback_query(call.id)
            return

        user = await get_user(call.from_user)
        _, code = unpack(call.data)

        if code not in i18n.languages:
            await bot.answer_callback_query(call.id, translate(user)("language.usage"), show_alert=True)
            return

        user.language = code
        await user.save()
        t = translate(user)
        await bot.answer_callback_query(call.id, t("language.changed", lang=code.upper()))
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"{t('language.changed', lang=code.upper())}\n\n{welcome_text(t, user.display_name, True)}",
            reply_markup=main_menu(t),
        )
