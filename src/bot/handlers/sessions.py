from __future__ import annotations

from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, Message
from telebot.util import extract_arguments

from bot.utils.storage import get_user, translate
from database import ChatSession
from telegram import inline, pack, unpack


def session_menu(sessions: list[ChatSession], current_id: int, t):
    rows = []
    for session in sessions:
        active = session.id == current_id
        title = session.title or t("session.untitled")
        mark = "✅" if active else "💬"
        rows.append(
            [
                (
                    f"{mark} {title}"[:60],
                    pack("session", "switch", session.id),
                    "success" if active else "primary",
                )
            ]
        )
    rows.append([(t("session.new"), pack("session", "new"), "success")])
    return inline(rows)


async def unpin(bot: AsyncTeleBot, chat_id: int, session: ChatSession) -> None:
    if not session.pinned_message_id:
        return
    try:
        await bot.unpin_chat_message(chat_id, message_id=session.pinned_message_id)
    except Exception:
        pass


async def pin_current(
    bot: AsyncTeleBot,
    chat_id: int,
    session: ChatSession,
    t,
    *,
    replace: bool = False,
) -> None:
    if session.pinned_message_id and not replace:
        return
    if replace:
        await unpin(bot, chat_id, session)

    markup = inline([[(t("session.open"), pack("session", "list"), "primary")]])
    message = await bot.send_message(
        chat_id,
        t("session.pinned", title=session.title or t("session.untitled")),
        reply_markup=markup,
    )
    try:
        await bot.pin_chat_message(chat_id, message.message_id, disable_notification=True)
    except Exception:
        pass
    session.pinned_message_id = message.message_id
    await session.save()


async def refresh_pinned(bot: AsyncTeleBot, chat_id: int, session: ChatSession, t) -> None:
    if not session.pinned_message_id:
        return
    markup = inline([[(t("session.open"), pack("session", "list"), "primary")]])
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=session.pinned_message_id,
            text=t("session.pinned", title=session.title or t("session.untitled")),
            reply_markup=markup,
        )
    except Exception:
        pass


async def show_sessions(bot: AsyncTeleBot, user, chat_id: int, t, message_id: int | None = None) -> None:
    current = await ChatSession.current(user.id, chat_id)
    sessions = await ChatSession.all_for(user.id, chat_id)
    markup = session_menu(sessions, current.id, t)
    text = f"{t('session.title')}\n\n{t('session.hint')}"

    if message_id is None:
        await bot.send_message(chat_id, text, reply_markup=markup)
    else:
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=markup)


def session_command(bot: AsyncTeleBot) -> None:
    @bot.message_handler(commands=["session"])
    async def _(message: Message) -> None:
        user = await get_user(message.from_user)
        t = translate(user)
        args = extract_arguments(message.text).strip()
        chat_id = message.chat.id

        if not args:
            await show_sessions(bot, user, chat_id, t)
            return

        action, _, rest = args.partition(" ")
        action = action.lower()
        rest = rest.strip()

        if action == "new":
            old = await ChatSession.current(user.id, chat_id)
            session = await ChatSession.new(user.id, chat_id, rest or None)
            await unpin(bot, chat_id, old)
            if message.chat.type == "private":
                await pin_current(bot, chat_id, session, t, replace=True)
            await bot.reply_to(
                message,
                t("session.created", title=session.title or t("session.untitled")),
                reply_markup=session_menu(await ChatSession.all_for(user.id, chat_id), session.id, t),
            )
            return

        if action == "title":
            if not rest:
                await bot.reply_to(message, t("session.usage"))
                return
            session = await ChatSession.current(user.id, chat_id)
            await session.set_title(rest)
            await refresh_pinned(bot, chat_id, session, t)
            await bot.reply_to(message, t("session.renamed", title=session.title))
            return

        await bot.reply_to(message, t("session.usage"))

    @bot.callback_query_handler(func=lambda call: call.data.startswith("session:"))
    async def _(call: CallbackQuery) -> None:
        user = await get_user(call.from_user)
        t = translate(user)
        parts = unpack(call.data)
        chat_id = call.message.chat.id

        if parts[1] == "list":
            await show_sessions(bot, user, chat_id, t)
            await bot.answer_callback_query(call.id)
            return

        if parts[1] == "new":
            old = await ChatSession.current(user.id, chat_id)
            session = await ChatSession.new(user.id, chat_id)
            await unpin(bot, chat_id, old)
            if call.message.chat.type == "private":
                await pin_current(bot, chat_id, session, t, replace=True)
            await show_sessions(bot, user, chat_id, t, call.message.message_id)
            await bot.answer_callback_query(call.id, t("session.created", title=session.title or t("session.untitled")))
            return

        if parts[1] == "switch":
            session = await ChatSession.get(id=int(parts[2]), user_id=user.id, chat_id=chat_id)
            if session is None:
                await bot.answer_callback_query(call.id, t("errors.unauthorized"), show_alert=True)
                return
            old = await ChatSession.current(user.id, chat_id)
            if old.id != session.id:
                await session.activate()
                await unpin(bot, chat_id, old)
                if call.message.chat.type == "private":
                    await pin_current(bot, chat_id, session, t, replace=True)
            await show_sessions(bot, user, chat_id, t, call.message.message_id)
            await bot.answer_callback_query(call.id, t("session.switched", title=session.title or t("session.untitled")))
