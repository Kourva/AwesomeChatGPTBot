from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from bot.utils.storage import get_user, translate
from telegram.markdown import escape


def help_text(t, username: str | None) -> str:
    return "\n".join(
        [
            t("help.title"),
            "",
            t("help.chat"),
            t("help.ping"),
            t("help.settings"),
            t("help.session"),
            t("help.history"),
            t("help.reset"),
            t("help.tts"),
            t("help.image"),
            t("help.danmode"),
            t("help.language"),
            t("help.upload"),
            "",
            t("help.roles", username=username or ""),
        ]
    )


def help_command(bot: AsyncTeleBot) -> None:
    @bot.message_handler(commands=["help"])
    async def _(message: Message) -> None:
        user = await get_user(message.from_user)
        t = translate(user)
        me = await bot.get_me()

        await bot.reply_to(
            message,
            escape(help_text(t, me.username)),
            parse_mode="MarkdownV2",
            disable_web_page_preview=True,
        )
