from __future__ import annotations

from .model import Model
from .models import (
    MODELS,
    ChatMessage,
    ChatSession,
    ChatSetting,
    KeyValue,
    ProviderSetting,
    Usage,
    User,
)
from .sqlite import Database


async def _upgrade(db: Database) -> None:
    columns = {row["name"] for row in await db.fetchall("PRAGMA table_info(messages)")}
    if "session_id" not in columns:
        await db.execute("ALTER TABLE messages ADD COLUMN session_id INTEGER")
    await db.execute("CREATE INDEX IF NOT EXISTS idx_messages_session ON messages (session_id, id)")

    rows = await db.fetchall("SELECT DISTINCT user_id, chat_id FROM messages WHERE session_id IS NULL")
    for row in rows:
        user_id = row["user_id"]
        chat_id = row["chat_id"] or user_id
        first = await db.fetchone(
            "SELECT content FROM messages WHERE user_id = ? AND chat_id IS ? AND role = 'user' ORDER BY id LIMIT 1",
            (user_id, row["chat_id"]),
        )
        title = ChatSession.title_from(first["content"]) if first else None
        await ChatSession.update({"user_id": user_id, "chat_id": chat_id}, active=0)
        session = await ChatSession.create(
            user_id=user_id,
            chat_id=chat_id,
            title=title,
            active=1,
            pinned_message_id=None,
        )
        await db.execute(
            "UPDATE messages SET session_id = ? WHERE user_id = ? AND chat_id IS ? AND session_id IS NULL",
            (session.id, user_id, row["chat_id"]),
        )


async def setup(path: str) -> Database:
    """ Connect, bind models and create every table."""
    db = Database(path)
    await db.connect()
    Model.bind(db)
    for model in MODELS:
        await model.migrate(db)
    await _upgrade(db)
    return db


__all__ = [
    "ChatMessage",
    "ChatSession",
    "ChatSetting",
    "Database",
    "KeyValue",
    "Model",
    "ProviderSetting",
    "Usage",
    "User",
    "setup",
]
