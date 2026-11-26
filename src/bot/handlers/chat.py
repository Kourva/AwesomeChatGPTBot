from __future__ import annotations

from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, Message
from telebot.util import extract_arguments

from bot.data.prompts import DAN_PROMPT
from bot.handlers.sessions import pin_current
from bot.utils.storage import get_user, translate
from config import global_config
from database import ChatMessage, ChatSession, ChatSetting, ProviderSetting, Usage, User
from logger import logger
from providers import manager
from telegram import Streamer, drafts, inline, pack, safe_delete, safe_edit, typing, unpack

DAN_KEY = "dan"
REGEN = "regen"

async def history_for(user: User, session: ChatSession) -> list[dict[str, str]]:
    messages = await ChatMessage.history(session.id, global_config["history_limit"])
    if await ChatSetting.fetch(user.id, DAN_KEY) == "1":
        messages.insert(0, {"role": "system", "content": DAN_PROMPT})
    return messages


async def prepare_session(bot: AsyncTeleBot, user: User, message: Message, prompt: str, t):
    session = await ChatSession.current(user.id, message.chat.id)
    if not session.title:
        await session.set_title(prompt)
    await session.touch()
    if message.chat.type == "private":
        try:
            await pin_current(bot, message.chat.id, session, t)
        except Exception:
            logger.warning("could not pin current session")
    return session


async def stream_answer(
    bot: AsyncTeleBot,
    user: User,
    t,
    chat_id: int,
    chat_type: str,
    messages: list[dict[str, str]],
    enabled: list[str],
    *,
    old_message_id: int | None = None,
) -> str | None:
    """ Streams one answer; the old message is replaced so rich text always applies."""
    if old_message_id is not None:
        await safe_delete(bot, chat_id, old_message_id)

    markup = inline([[(t("common.regenerate"), pack(REGEN, user.id), "primary")]])
    private = chat_type == "private"
    streamer = Streamer(
        bot,
        chat_id,
        draft_id=drafts.new_id() if private else None,
        is_rtl=user.language == "fa",
        reply_markup=markup,
        placeholder=t("common.thinking"),
    )
    if not private:
        placeholder = await bot.send_message(chat_id, t("common.thinking"))
        streamer.message_id = placeholder.message_id

    try:
        async with typing(bot, chat_id):
            return await streamer.run(manager.stream(messages, enabled=enabled))
    except Exception:
        logger.exception(f"providers failed for user {user.id}")
        await Usage.bump(user.id, "errors")
        error = t("errors.providers_down")
        if streamer.message_id is not None:
            await safe_edit(bot, chat_id, streamer.message_id, error)
        else:
            await bot.send_message(chat_id, error)
        return None


def chat_command(bot: AsyncTeleBot) -> None:
    async def respond(message: Message, prompt: str) -> None:
        user = await get_user(message.from_user)
        t = translate(user)
        enabled = await ProviderSetting.enabled_for(user.id)

        if not enabled:
            await bot.reply_to(message, t("errors.providers_down"))
            return

        session = await prepare_session(bot, user, message, prompt, t)
        await ChatMessage.create(
            user_id=user.id,
            chat_id=message.chat.id,
            session_id=session.id,
            role="user",
            content=prompt,
        )

        answer = await stream_answer(
            bot,
            user,
            t,
            message.chat.id,
            message.chat.type,
            await history_for(user, session),
            enabled,
        )
        if answer is None:
            return

        if answer.strip():
            await ChatMessage.create(
                user_id=user.id,
                chat_id=message.chat.id,
                session_id=session.id,
                role="assistant",
                content=answer,
            )
        await Usage.bump(user.id)

    @bot.message_handler(commands=["chat"])
    async def _(message: Message) -> None:
        prompt = extract_arguments(message.text).strip()
        if not prompt:
            user = await get_user(message.from_user)
            await bot.reply_to(message, translate(user)("chat.usage"))
            return
        await respond(message, prompt)

    @bot.message_handler(
        func=lambda m: m.chat.type == "private" and not (m.text or "").startswith("/"),
        content_types=["text"],
    )
    async def _(message: Message) -> None:
        await respond(message, (message.text or "").strip())

    @bot.callback_query_handler(func=lambda call: call.data.startswith(f"{REGEN}:"))
    async def _(call: CallbackQuery) -> None:
        user = await get_user(call.from_user)
        t = translate(user)
        _, owner = unpack(call.data)

        if int(owner) != user.id:
            await bot.answer_callback_query(call.id, t("errors.unauthorized"), show_alert=True)
            return

        session = await ChatSession.current(user.id, call.message.chat.id)
        recent = await ChatMessage.filter(session_id=session.id, order_by="id DESC", limit=2)
        prompt = next((row for row in recent if row.role == "user"), None)
        if prompt is None:
            await bot.answer_callback_query(call.id, t("history.empty"), show_alert=True)
            return

        enabled = await ProviderSetting.enabled_for(user.id)
        if not enabled:
            await bot.answer_callback_query(call.id, t("errors.providers_down"), show_alert=True)
            return

        answer_row = next((row for row in recent if row.role == "assistant"), None)
        if answer_row is not None:
            await answer_row.delete_row()

        await bot.answer_callback_query(call.id)
        answer = await stream_answer(
            bot,
            user,
            t,
            call.message.chat.id,
            call.message.chat.type,
            await history_for(user, session),
            enabled,
            old_message_id=call.message.message_id,
        )
        if answer is None:
            return

        if answer.strip():
            await ChatMessage.create(
                user_id=user.id,
                chat_id=call.message.chat.id,
                session_id=session.id,
                role="assistant",
                content=answer,
            )
        await Usage.bump(user.id)


def dan_mode_command(bot: AsyncTeleBot) -> None:
    @bot.message_handler(commands=["danmode"])
    async def _(message: Message) -> None:
        user = await get_user(message.from_user)
        t = translate(user)
        current = await ChatSetting.fetch(user.id, DAN_KEY)
        session = await ChatSession.current(user.id, message.chat.id)

        await ChatSetting.put(user.id, DAN_KEY, "0" if current == "1" else "1")
        await ChatMessage.delete(session_id=session.id)
        await bot.reply_to(message, t("chat.dan_off" if current == "1" else "chat.dan_on"))
