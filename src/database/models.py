from __future__ import annotations

import time
from collections.abc import Iterable
from datetime import datetime, timezone
from typing import Any

from .model import Model


class User(Model):
    table = "users"
    fields = {
        "id": "INTEGER PRIMARY KEY",
        "username": "TEXT",
        "first_name": "TEXT",
        "last_name": "TEXT",
        "language": "TEXT DEFAULT 'en'",
        "is_banned": "INTEGER DEFAULT 0",
        "created_at": "TEXT",
        "updated_at": "TEXT",
    }

    @property
    def display_name(self) -> str:
        return self.first_name or self.username or str(self.id)


class ChatSession(Model):
    table = "sessions"
    fields = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "user_id": "INTEGER NOT NULL",
        "chat_id": "INTEGER NOT NULL",
        "title": "TEXT",
        "active": "INTEGER DEFAULT 0",
        "pinned_message_id": "INTEGER",
        "created_at": "TEXT",
        "updated_at": "TEXT",
    }
    indexes = (
        "CREATE INDEX IF NOT EXISTS idx_sessions_chat ON sessions (user_id, chat_id, id)",
    )

    @staticmethod
    def title_from(text: str) -> str:
        line = " ".join((text or "").split())
        return (line[:47] + "…") if len(line) > 48 else (line or "New chat")

    @classmethod
    async def current(cls, user_id: int, chat_id: int) -> ChatSession:
        row = await cls.get(user_id=user_id, chat_id=chat_id, active=1)
        if row is not None:
            return row

        rows = await cls.filter(user_id=user_id, chat_id=chat_id, order_by="id DESC", limit=1)
        if rows:
            rows[0].active = 1
            await rows[0].save()
            return rows[0]

        return await cls.create(
            user_id=user_id,
            chat_id=chat_id,
            title=None,
            active=1,
            pinned_message_id=None,
        )

    @classmethod
    async def all_for(cls, user_id: int, chat_id: int) -> list[ChatSession]:
        return await cls.filter(user_id=user_id, chat_id=chat_id, order_by="id DESC")

    @classmethod
    async def new(cls, user_id: int, chat_id: int, title: str | None = None) -> ChatSession:
        await cls.update({"user_id": user_id, "chat_id": chat_id}, active=0)
        return await cls.create(
            user_id=user_id,
            chat_id=chat_id,
            title=title,
            active=1,
            pinned_message_id=None,
        )

    async def activate(self) -> None:
        await self.update({"user_id": self.user_id, "chat_id": self.chat_id}, active=0)
        self.active = 1
        await self.save()

    async def set_title(self, title: str) -> None:
        self.title = self.title_from(title)
        await self.save()

    async def touch(self) -> None:
        await self.save()


class ChatMessage(Model):
    table = "messages"
    fields = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "user_id": "INTEGER NOT NULL",
        "chat_id": "INTEGER",
        "session_id": "INTEGER",
        "role": "TEXT NOT NULL",
        "content": "TEXT NOT NULL",
        "provider": "TEXT",
        "created_at": "TEXT",
    }
    indexes = (
        "CREATE INDEX IF NOT EXISTS idx_messages_user ON messages (user_id, id)",
    )

    @classmethod
    async def history(cls, session_id: int, limit: int = 20) -> list[dict[str, str]]:
        rows = await cls.filter(session_id=session_id, order_by="id DESC", limit=limit)
        return [{"role": row.role, "content": row.content} for row in reversed(rows)]


class ProviderSetting(Model):
    table = "provider_settings"
    fields = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "user_id": "INTEGER NOT NULL",
        "provider": "TEXT NOT NULL",
        "enabled": "INTEGER DEFAULT 1",
        "model": "TEXT",
        "created_at": "TEXT",
        "updated_at": "TEXT",
    }
    unique = (("user_id", "provider"),)

    @classmethod
    async def seed(cls, user_id: int, providers: Iterable[str]) -> None:
        for name in providers:
            if not await cls.get(user_id=user_id, provider=name):
                await cls.create(user_id=user_id, provider=name, enabled=1)

    @classmethod
    async def enabled_for(cls, user_id: int) -> list[str]:
        rows = await cls.filter(user_id=user_id, enabled=1, order_by="id")
        return [row.provider for row in rows]

    @classmethod
    async def toggle(cls, user_id: int, provider: str) -> bool:
        row = await cls.get(user_id=user_id, provider=provider)
        if row is None:
            await cls.create(user_id=user_id, provider=provider, enabled=0)
            return False
        row.enabled = 0 if row.enabled else 1
        await row.save()
        return bool(row.enabled)


class Usage(Model):
    table = "usage"
    fields = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "user_id": "INTEGER NOT NULL",
        "day": "TEXT NOT NULL",
        "requests": "INTEGER DEFAULT 0",
        "errors": "INTEGER DEFAULT 0",
    }
    unique = (("user_id", "day"),)

    @classmethod
    async def bump(cls, user_id: int, field: str = "requests") -> None:
        if field not in cls.fields or field == "id":
            raise ValueError(f"unknown counter: {field}")
        day = datetime.now(timezone.utc).date().isoformat()
        row = await cls.get(user_id=user_id, day=day)
        if row is None:
            await cls.create(user_id=user_id, day=day, **{field: 1})
        else:
            await cls.db().execute(
                f"UPDATE usage SET {field} = {field} + 1 WHERE id = ?",
                (row.id,),
            )


class KeyValue(Model):
    table = "key_values"
    primary_key = "key"
    fields = {
        "key": "TEXT PRIMARY KEY",
        "value": "TEXT",
        "expires_at": "TEXT",
    }

    @classmethod
    async def put(cls, key: str, value: Any, ttl: int | None = None) -> None:
        expires = str(time.time() + ttl) if ttl else None
        row = await cls.get(key=key)
        if row is None:
            await cls.create(key=key, value=str(value), expires_at=expires)
        else:
            row.value = str(value)
            row.expires_at = expires
            await row.save()

    @classmethod
    async def fetch(cls, key: str) -> str | None:
        row = await cls.get(key=key)
        if row is None:
            return None
        if row.expires_at and float(row.expires_at) < time.time():
            await row.delete_row()
            return None
        return row.value


class ChatSetting(Model):
    table = "chat_settings"
    fields = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "chat_id": "INTEGER NOT NULL",
        "key": "TEXT NOT NULL",
        "value": "TEXT",
    }
    unique = (("chat_id", "key"),)

    @classmethod
    async def put(cls, chat_id: int, key: str, value: Any) -> None:
        row = await cls.get(chat_id=chat_id, key=key)
        if row is None:
            await cls.create(chat_id=chat_id, key=key, value=str(value))
        else:
            row.value = str(value)
            await row.save()

    @classmethod
    async def fetch(cls, chat_id: int, key: str, default: str | None = None) -> str | None:
        row = await cls.get(chat_id=chat_id, key=key)
        return row.value if row else default


MODELS = (User, ChatSession, ChatMessage, ProviderSetting, Usage, KeyValue, ChatSetting)
