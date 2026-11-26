from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager, suppress

from telebot.apihelper import ApiTelegramException

FENCE = "```"


def split_message(text: str, limit: int = 4096) -> list[str]:
    """ Splits long text on newlines and closes open code blocks."""
    if len(text) <= limit:
        return [text]

    parts: list[str] = []
    rest = text

    while rest:
        if len(rest) <= limit:
            parts.append(rest)
            break

        cut = rest.rfind("\n", 0, limit)
        if cut < limit // 2:
            cut = limit

        chunk, rest = rest[:cut], rest[cut:].lstrip("\n")
        if chunk.count(FENCE) % 2:
            chunk += "\n" + FENCE
            rest = FENCE + "\n" + rest
        parts.append(chunk)

    return parts


async def safe_edit(bot, chat_id: int, message_id: int, text: str, **kwargs):
    """ Edits a message, retries plain text when MarkdownV2 breaks."""
    try:
        return await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            **kwargs,
        )
    except ApiTelegramException as exc:
        if "not modified" in str(exc).lower():
            return None
        if kwargs.get("parse_mode"):
            retry = {**kwargs, "parse_mode": None}
            try:
                return await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=text,
                    **retry,
                )
            except ApiTelegramException:
                return None
        return None


async def safe_delete(bot, chat_id: int, message_id: int) -> None:
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except ApiTelegramException:
        pass


@asynccontextmanager
async def typing(bot, chat_id: int, action: str = "typing", interval: float = 4.5):
    """ Keeps the typing indicator alive while a slow task runs."""

    async def loop() -> None:
        while True:
            with suppress(Exception):
                await bot.send_chat_action(chat_id=chat_id, action=action)
            await asyncio.sleep(interval)

    task = asyncio.create_task(loop())
    try:
        yield
    finally:
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task
