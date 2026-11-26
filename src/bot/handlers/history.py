from __future__ import annotations

import io
import json

from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, InputFile, Message

from bot.utils.storage import get_user, translate
from database import ChatMessage, ChatSession
from telegram import inline, pack, unpack


def history_menu(sessions: list[ChatSession], t):
    rows = [
        [
            (
                f"🗂 {(session.title or t('session.untitled'))[:40]}",
                pack("hist", "get", session.id),
                "primary",
            )
        ]
        for session in sessions
    ]
    rows.append([(t("common.back"), pack("menu", "back"), "primary")])
    return inline(rows)


def stamp(value: str | None) -> str:
    return (value or "").replace("T", " ")[:16]


def caption_for(session: ChatSession, rows: list[ChatMessage], t) -> str:
    you = sum(1 for row in rows if row.role == "user")
    return t(
        "history.caption",
        title=session.title or t("session.untitled"),
        id=session.id,
        state=t("history.active" if session.active else "history.inactive"),
        count=len(rows),
        you=you,
        ai=len(rows) - you,
        started=stamp(session.created_at),
        updated=stamp(session.updated_at),
    )


async def send_history(
    bot: AsyncTeleBot,
    t,
    chat_id: int,
    session: ChatSession,
    reply_to: int | None = None,
) -> bool:
    rows = await ChatMessage.filter(session_id=session.id, order_by="id")
    if not rows:
        return False

    payload = json.dumps([row.to_dict() for row in rows], indent=2, ensure_ascii=False)
    document = InputFile(io.BytesIO(payload.encode()), f"chat-{session.id}.json")
    await bot.send_document(
        chat_id,
        document,
        caption=caption_for(session, rows, t),
        reply_to_message_id=reply_to,
    )
    return True


async def show_history_menu(
    bot: AsyncTeleBot,
    user,
    t,
    chat_id: int,
    message_id: int | None = None,
) -> None:
    sessions = await ChatSession.all_for(user.id, chat_id)
    text = f"{t('history.title')}\n\n{t('history.hint')}" if sessions else t("history.empty")
    markup = history_menu(sessions, t)

    if message_id is None:
        await bot.send_message(chat_id, text, reply_markup=markup)
    else:
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=markup)


def history_command(bot: AsyncTeleBot) -> None:
    @bot.message_handler(commands=["history"])
    async def _(message: Message) -> None:
        user = await get_user(message.from_user)
        t = translate(user)
        await show_history_menu(bot, user, t, message.chat.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("hist:"))
    async def _(call: CallbackQuery) -> None:
        user = await get_user(call.from_user)
        t = translate(user)
        parts = unpack(call.data)
        chat_id = call.message.chat.id

        if parts[1] == "menu":
            await show_history_menu(bot, user, t, chat_id, call.message.message_id)
            await bot.answer_callback_query(call.id)
            return

        if parts[1] != "get" or len(parts) < 3:
            await bot.answer_callback_query(call.id, t("errors.unknown"), show_alert=True)
            return

        session = await ChatSession.get(id=int(parts[2]), user_id=user.id, chat_id=chat_id)
        if session is None:
            await bot.answer_callback_query(call.id, t("errors.unauthorized"), show_alert=True)
            return

        if not await send_history(bot, t, chat_id, session):
            await bot.answer_callback_query(call.id, t("history.empty"), show_alert=True)
            return

        await bot.answer_callback_query(call.id, t("history.sent"))


def reset_command(bot: AsyncTeleBot) -> None:
    @bot.message_handler(commands=["reset"])
    async def _(message: Message) -> None:
        user = await get_user(message.from_user)
        t = translate(user)
        session = await ChatSession.current(user.id, message.chat.id)
        await ChatMessage.delete(session_id=session.id)
        await bot.reply_to(message, t("history.cleared"))
