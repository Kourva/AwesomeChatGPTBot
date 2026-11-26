from telebot.async_telebot import AsyncTeleBot

from bot.handlers import (
    chat_command,
    dan_mode_command,
    help_command,
    history_command,
    image_command,
    language_command,
    ping_command,
    reset_command,
    session_command,
    settings_command,
    start_command,
    tpdne_command,
    tts_command,
    upload_handler,
)
from bot.inlines import roles_inline, web_search_inline
from logger import logger
from telegram import drafts


def register(bot: AsyncTeleBot) -> None:
    start_command(bot)
    help_command(bot)
    ping_command(bot)
    settings_command(bot)
    session_command(bot)
    history_command(bot)
    reset_command(bot)
    language_command(bot)
    image_command(bot)
    tts_command(bot)
    tpdne_command(bot)
    upload_handler(bot)
    dan_mode_command(bot)

    # keep this last after commands
    chat_command(bot)

    roles_inline(bot)
    web_search_inline(bot)

    @bot.stopped_message_generation_handler()
    async def _(stopped) -> None:
        drafts.cancel(stopped.draft_id)

    logger.info("Handlers and callbacks registered")
