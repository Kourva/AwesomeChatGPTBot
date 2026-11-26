from __future__ import annotations

import base64
import io
import os

from telebot.async_telebot import AsyncTeleBot
from telebot.types import InputFile, Message
from telebot.util import extract_arguments

from bot.handlers.chat import history_for, prepare_session, stream_answer
from bot.utils.storage import get_user, translate
from config import global_config
from database import ChatMessage, ProviderSetting, Usage
from logger import logger
from providers import manager, pollinations, tts
from telegram import typing

TEXT_SUFFIXES = {
    ".txt", ".md", ".markdown", ".json", ".csv", ".log", ".py", ".js", ".ts",
    ".html", ".css", ".xml", ".yaml", ".yml", ".ini", ".conf", ".sh", ".sql", ".toml",
}
MAX_BYTES = 20 * 1024 * 1024
MAX_TEXT = 12000


def upload_target(message: Message) -> tuple[str, str, str]:
    if message.photo:
        return message.photo[-1].file_id, "image/jpeg", "photo.jpg"
    document = message.document
    return (
        document.file_id,
        document.mime_type or "",
        document.file_name or "file",
    )


def is_text_upload(name: str, mime: str) -> bool:
    return (
        os.path.splitext(name)[1].lower() in TEXT_SUFFIXES
        or mime.startswith("text/")
        or mime in ("application/json", "application/xml")
    )


async def read_upload(bot: AsyncTeleBot, message: Message) -> bytes:
    file_id, _, _ = upload_target(message)
    info = await bot.get_file(file_id)
    if (info.file_size or 0) > MAX_BYTES:
        raise ValueError("file is too large")
    return await bot.download_file(info.file_path)


def image_parts(prompt: str, data: bytes, mime: str) -> list[dict]:
    encoded = base64.b64encode(data).decode()
    return [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": f"data:{mime or 'image/jpeg'};base64,{encoded}"}},
    ]


def image_command(bot: AsyncTeleBot) -> None:
    @bot.message_handler(commands=["image"])
    async def _(message: Message) -> None:
        user = await get_user(message.from_user)
        t = translate(user)
        prompt = extract_arguments(message.text).strip()

        if not prompt:
            await bot.reply_to(message, t("image.usage"))
            return

        await bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")
        try:
            await bot.send_photo(
                message.chat.id,
                photo=pollinations.image(prompt),
                reply_to_message_id=message.message_id,
                caption=prompt,
            )
        except Exception:
            logger.exception(f"image failed for user {user.id}")
            await bot.reply_to(message, t("image.error"))


def upload_handler(bot: AsyncTeleBot) -> None:
    @bot.message_handler(content_types=["photo", "document"])
    async def _(message: Message) -> None:
        user = await get_user(message.from_user)
        t = translate(user)
        enabled = await ProviderSetting.enabled_for(user.id)

        if not enabled:
            await bot.reply_to(message, t("errors.providers_down"))
            return

        _, mime, name = upload_target(message)
        photo = bool(message.photo) or mime.startswith("image/")
        text_file = not photo and is_text_upload(name, mime)

        if not photo and not text_file:
            await bot.reply_to(message, t("media.unsupported"))
            return

        if photo and not manager.vision_ready(enabled):
            await bot.reply_to(message, t("media.no_vision"))
            return

        prompt = (message.caption or "").strip()
        prompt = prompt or t("media.default_image" if photo else "media.default_file")

        try:
            data = await read_upload(bot, message)
        except ValueError:
            await bot.reply_to(message, t("media.too_large"))
            return
        except Exception:
            logger.exception(f"upload failed for user {user.id}")
            await bot.reply_to(message, t("media.failed"))
            return

        session = await prepare_session(bot, user, message, prompt, t)
        await ChatMessage.create(
            user_id=user.id,
            chat_id=message.chat.id,
            session_id=session.id,
            role="user",
            content=f"{prompt}\n\n[{name}]",
        )

        messages = await history_for(user, session)
        if photo:
            messages[-1] = {"role": "user", "content": image_parts(prompt, data, mime)}
        else:
            text = data.decode("utf-8", errors="replace")[:MAX_TEXT]
            messages[-1] = {"role": "user", "content": f"{prompt}\n\n---\n{text}"}

        answer = await stream_answer(
            bot,
            user,
            t,
            message.chat.id,
            message.chat.type,
            messages,
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


def tts_command(bot: AsyncTeleBot) -> None:
    @bot.message_handler(commands=["tts"])
    async def _(message: Message) -> None:
        user = await get_user(message.from_user)
        t = translate(user)
        text = extract_arguments(message.text).strip()

        if not text:
            await bot.reply_to(message, t("tts.usage"))
            return

        try:
            async with typing(bot, message.chat.id, "record_voice"):
                audio = await tts.say(text, voice=global_config["tts_voice"], language=user.language or "en")
                await bot.send_voice(
                    message.chat.id,
                    voice=InputFile(io.BytesIO(audio), "voice.mp3"),
                    caption=text[:200],
                    reply_to_message_id=message.message_id,
                )
        except Exception:
            logger.exception(f"tts failed for user {user.id}")
            await bot.reply_to(message, t("tts.error"))


def tpdne_command(bot: AsyncTeleBot) -> None:
    @bot.message_handler(commands=["tpdne"])
    async def _(message: Message) -> None:
        user = await get_user(message.from_user)
        t = translate(user)
        await bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")
        try:
            await bot.send_photo(
                message.chat.id,
                photo="https://thispersondoesnotexist.com",
                caption=t("media.tpdne"),
                reply_to_message_id=message.message_id,
                has_spoiler=True,
            )
        except Exception:
            logger.exception(f"tpdne failed for user {user.id}")
            await bot.reply_to(message, t("image.error"))
