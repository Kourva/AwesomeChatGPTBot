from __future__ import annotations

import time
from collections.abc import AsyncIterator
from contextlib import suppress

from telebot.types import InputRichMessage

from . import drafts
from .formatting import safe_delete, safe_edit, split_message


class Streamer:
    """ Streams a rich answer. """

    def __init__(
        self,
        bot,
        chat_id: int,
        message_id: int | None = None,
        *,
        draft_id: int | None = None,
        interval: float = 1.0,
        limit: int = 30000,
        reply_markup=None,
        cursor: str = "⋯",
        placeholder: str = "Hmmmm",
        can_stop: bool = True,
        is_rtl: bool = False,
    ) -> None:
        self.bot = bot
        self.chat_id = chat_id
        self.message_id = message_id
        self.draft_id = draft_id
        self.interval = interval
        self.limit = limit
        self.reply_markup = reply_markup
        self.cursor = cursor
        self.placeholder = placeholder
        self.can_stop = can_stop
        self.is_rtl = is_rtl

        self.buffer = ""
        self.shown = ""
        self.extra: list[int] = []
        self.last_edit = 0.0
        self.stopped = False
        self.rich_draft = bool(draft_id)
        self.stop_id = draft_id
        self.stop = drafts.register(draft_id) if draft_id else None

    async def run(self, chunks: AsyncIterator[str]) -> str:
        if self.draft_id:
            try:
                await self._draft("")
            except Exception:
                self.draft_id = None
                self.rich_draft = False

        if self.message_id is None and self.draft_id is None:
            message = await self.bot.send_message(self.chat_id, self.placeholder)
            self.message_id = message.message_id

        try:
            async for chunk in chunks:
                if self.stop is not None and self.stop.is_set():
                    self.stopped = True
                    break
                if not chunk:
                    continue
                self.buffer += chunk
                now = time.monotonic()
                if now - self.last_edit >= self.interval:
                    await self._preview()
                    self.last_edit = now

            if not self.stopped or self.buffer.strip():
                await self._finish()
            return self.buffer
        finally:
            if self.stop_id:
                drafts.unregister(self.stop_id)
            if self.stopped and hasattr(chunks, "aclose"):
                with suppress(Exception):
                    await chunks.aclose()

    async def _draft(self, text: str) -> None:
        if not self.draft_id:
            return

        if self.rich_draft and text:
            try:
                await self.bot.send_rich_message_draft(
                    self.chat_id,
                    self.draft_id,
                    InputRichMessage(markdown=text, is_rtl=self.is_rtl),
                    can_stop=self.can_stop,
                    keep_on_stop=False,
                )
                return
            except Exception:
                self.rich_draft = False

        await self.bot.send_message_draft(
            self.chat_id,
            self.draft_id,
            text or self.placeholder,
            can_stop=self.can_stop,
            keep_on_stop=False,
        )

    async def _preview(self) -> None:
        text = self.buffer
        if len(text) > self.limit:
            text = text[: self.limit - len(self.cursor)]
        preview = text + self.cursor
        if preview == self.shown:
            return

        if self.draft_id:
            try:
                await self._draft(preview)
            except Exception:
                return
        else:
            await safe_edit(self.bot, self.chat_id, self.message_id, preview)
        self.shown = preview

    async def _finish(self) -> None:
        if self.message_id is not None:
            await safe_delete(self.bot, self.chat_id, self.message_id)
            self.message_id = None

        text = self.buffer.strip() or self.placeholder
        parts = split_message(text, self.limit)
        for index, part in enumerate(parts):
            markup = self.reply_markup if index == len(parts) - 1 else None
            message = await self._send_rich(part, markup)
            if self.message_id is None:
                self.message_id = message.message_id
            else:
                self.extra.append(message.message_id)

    async def _send_rich(self, text: str, markup):
        try:
            return await self.bot.send_rich_message(
                self.chat_id,
                InputRichMessage(markdown=text, is_rtl=self.is_rtl),
                reply_markup=markup,
            )
        except Exception:
            return await self.bot.send_message(self.chat_id, text, reply_markup=markup)
