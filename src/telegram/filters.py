from __future__ import annotations

from telebot.apihelper import ApiTelegramException
from telebot.types import Message


def private(message: Message) -> bool:
    return message.chat.type == "private"


def group(message: Message) -> bool:
    return message.chat.type in ("group", "supergroup")


def sudo(admin_id: int | str):
    """ Returns a filter for message handlers."""

    def check(message: Message) -> bool:
        return bool(message.from_user) and message.from_user.id == int(admin_id)

    return check


async def is_admin(bot, chat_id: int, user_id: int) -> bool:
    try:
        admins = await bot.get_chat_administrators(chat_id)
    except ApiTelegramException:
        return False
    return any(admin.user.id == user_id for admin in admins)
