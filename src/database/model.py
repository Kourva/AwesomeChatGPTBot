from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Self

from .sqlite import Database


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Model:
    """ Small active record layer, Django style methods over SQLite."""

    table: str = ""
    fields: dict[str, str] = {}
    primary_key: str = "id"
    unique: tuple[tuple[str, ...], ...] = ()
    indexes: tuple[str, ...] = ()
    _db: Database | None = None

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = dict(data)

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self._data}>"

    def __getattr__(self, name: str) -> Any:
        data = self.__dict__.get("_data", {})
        if name in data:
            return data[name]
        raise AttributeError(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "_data":
            object.__setattr__(self, name, value)
        else:
            self._data[name] = value

    def to_dict(self) -> dict[str, Any]:
        return dict(self._data)

    @classmethod
    def bind(cls, db: Database) -> None:
        Model._db = db

    @classmethod
    def db(cls) -> Database:
        if Model._db is None:
            raise RuntimeError("call Model.bind(db) or database.setup() first")
        return Model._db

    @classmethod
    async def migrate(cls, db: Database | None = None) -> None:
        db = db or cls.db()
        columns = ", ".join(f"{name} {sql}" for name, sql in cls.fields.items())
        rules = [f"UNIQUE ({', '.join(group)})" for group in cls.unique]
        body = ", ".join([columns, *rules])
        await db.execute(f"CREATE TABLE IF NOT EXISTS {cls.table} ({body})")
        for statement in cls.indexes:
            await db.execute(statement)

    @classmethod
    async def create(cls, **values: Any) -> Self:
        now = utcnow()
        for stamp in ("created_at", "updated_at"):
            if stamp in cls.fields and stamp not in values:
                values[stamp] = now

        columns = ", ".join(values)
        marks = ", ".join("?" for _ in values)
        rowid = await cls.db().execute(
            f"INSERT INTO {cls.table} ({columns}) VALUES ({marks})",
            tuple(values.values()),
        )
        if cls.primary_key == "id" and "id" not in values:
            values["id"] = rowid
        return cls(values)

    @classmethod
    async def get(cls, **where: Any) -> Self | None:
        clause, params = cls._where(where)
        row = await cls.db().fetchone(f"SELECT * FROM {cls.table}{clause}", params)
        return cls(row) if row is not None else None

    @classmethod
    async def filter(
        cls,
        *,
        order_by: str | None = None,
        limit: int | None = None,
        **where: Any,
    ) -> list[Self]:
        clause, params = cls._where(where)
        sql = f"SELECT * FROM {cls.table}{clause}"

        if order_by:
            column, _, direction = order_by.partition(" ")
            if column not in cls.fields:
                raise ValueError(f"unknown column: {column}")
            sql += f" ORDER BY {column} {'DESC' if direction.lower() == 'desc' else 'ASC'}"

        if limit is not None:
            sql += " LIMIT ?"
            params = (*params, int(limit))

        rows = await cls.db().fetchall(sql, params)
        return [cls(row) for row in rows]

    @classmethod
    async def update(cls, where: dict[str, Any], **values: Any) -> int:
        clause, params = cls._where(where)
        if "updated_at" in cls.fields:
            values["updated_at"] = utcnow()
        assignments = ", ".join(f"{name} = ?" for name in values)
        return await cls.db().execute(
            f"UPDATE {cls.table} SET {assignments}{clause}",
            (*values.values(), *params),
        )

    @classmethod
    async def delete(cls, **where: Any) -> int:
        clause, params = cls._where(where)
        return await cls.db().execute(f"DELETE FROM {cls.table}{clause}", params)

    @classmethod
    async def count(cls, **where: Any) -> int:
        clause, params = cls._where(where)
        row = await cls.db().fetchone(f"SELECT COUNT(*) AS total FROM {cls.table}{clause}", params)
        return int(row["total"]) if row else 0

    async def save(self) -> None:
        key = self._data.get(self.primary_key)
        if key is None:
            raise ValueError(f"cannot save a row without {self.primary_key}")

        skip = (self.primary_key, "created_at")
        values = {name: value for name, value in self._data.items() if name not in skip}
        if "updated_at" in self.fields:
            values["updated_at"] = utcnow()

        assignments = ", ".join(f"{name} = ?" for name in values)
        await self.db().execute(
            f"UPDATE {self.table} SET {assignments} WHERE {self.primary_key} = ?",
            (*values.values(), key),
        )

    async def delete_row(self) -> None:
        key = self._data.get(self.primary_key)
        if key is None:
            raise ValueError(f"cannot delete a row without {self.primary_key}")
        await self.db().execute(
            f"DELETE FROM {self.table} WHERE {self.primary_key} = ?",
            (key,),
        )

    @classmethod
    def _where(cls, where: dict[str, Any]) -> tuple[str, tuple[Any, ...]]:
        for name in where:
            if name not in cls.fields:
                raise ValueError(f"unknown column: {name}")
        if not where:
            return "", ()
        clause = " WHERE " + " AND ".join(f"{name} = ?" for name in where)
        return clause, tuple(where.values())
