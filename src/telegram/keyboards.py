from __future__ import annotations

from typing import Any, Iterable

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

SEP = ":"


def pack(*parts: Any) -> str:
    """ Builds callback data, max 64 bytes for Telegram limit."""
    data = SEP.join(str(part) for part in parts)
    if len(data.encode()) > 64:
        raise ValueError("callback data is longer than 64 bytes")
    return data


def unpack(data: str) -> list[str]:
    return data.split(SEP)


def inline(rows: Iterable[Iterable[tuple[str, str] | tuple[str, str, str]]]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    for row in rows:
        buttons = []
        for text, data, *style in row:
            buttons.append(
                InlineKeyboardButton(text=text, callback_data=data, style=style[0] if style else None)
            )
        markup.row(*buttons)
    return markup
