from __future__ import annotations

import asyncio
import sqlite3
from typing import Any

Params = tuple[Any, ...]


class Database:
    """ One async wrapper around sqlite3, safe for the bot event loop."""

    def __init__(self, path: str = "bot.db") -> None:
        self.path = path
        self._conn: sqlite3.Connection | None = None
        self._lock = asyncio.Lock()

    async def connect(self) -> Database:
        if self._conn is None:
            self._conn = sqlite3.connect(self.path, check_same_thread=False, timeout=30)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
        return self

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            raise RuntimeError("database is not connected")
        return self._conn

    async def execute(self, sql: str, params: Params = ()) -> int:
        """ Returns lastrowid for inserts, rowcount for the rest."""
        async with self._lock:
            return await asyncio.to_thread(self._execute, sql, params)

    def _execute(self, sql: str, params: Params) -> int:
        cursor = self.conn.execute(sql, params)
        self.conn.commit()
        return cursor.lastrowid if cursor.lastrowid is not None else cursor.rowcount

    async def fetchone(self, sql: str, params: Params = ()) -> dict[str, Any] | None:
        async with self._lock:
            row = await asyncio.to_thread(lambda: self.conn.execute(sql, params).fetchone())
        return dict(row) if row is not None else None

    async def fetchall(self, sql: str, params: Params = ()) -> list[dict[str, Any]]:
        async with self._lock:
            rows = await asyncio.to_thread(lambda: self.conn.execute(sql, params).fetchall())
        return [dict(row) for row in rows]

    async def close(self) -> None:
        if self._conn is not None:
            await asyncio.to_thread(self._conn.close)
            self._conn = None
