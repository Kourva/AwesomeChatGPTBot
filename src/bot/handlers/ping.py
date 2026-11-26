import json

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from bot.utils.storage import get_user, translate
from database import KeyValue
from providers import manager
from telegram import safe_edit, typing
from telegram.markdown import escape

CACHE_KEY = "provider:status"
CACHE_TTL = 60


def status_text(status: dict[str, bool], t) -> str:
    lines = [t("ping.title"), ""]
    for name, online in status.items():
        provider = manager.get(name)
        label = provider.label if provider else name
        lines.append(f"{label}: {t('ping.online' if online else 'ping.offline')}")
    return "\n".join(lines)


def ping_command(bot: AsyncTeleBot) -> None:
    @bot.message_handler(commands=["ping"])
    async def _(message: Message) -> None:
        user = await get_user(message.from_user)
        t = translate(user)
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")

        cached = await KeyValue.fetch(CACHE_KEY)
        if cached:
            try:
                status = json.loads(cached)
                await bot.reply_to(message, escape(status_text(status, t)), parse_mode="MarkdownV2")
                return
            except ValueError:
                pass

        placeholder = await bot.reply_to(message, t("ping.checking"))
        async with typing(bot, message.chat.id):
            status = await manager.ping()

        await KeyValue.put(CACHE_KEY, json.dumps(status), ttl=CACHE_TTL)
        await safe_edit(
            bot,
            message.chat.id,
            placeholder.message_id,
            escape(status_text(status, t)),
            parse_mode="MarkdownV2",
        )
