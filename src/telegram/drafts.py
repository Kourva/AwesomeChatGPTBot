from __future__ import annotations

import asyncio
import secrets

_events: dict[int, asyncio.Event] = {}


def new_id() -> int:
    return secrets.randbits(31) or 1


def register(draft_id: int) -> asyncio.Event:
    event = asyncio.Event()
    _events[draft_id] = event
    return event


def cancel(draft_id: int) -> None:
    event = _events.get(draft_id)
    if event is not None:
        event.set()


def unregister(draft_id: int) -> None:
    _events.pop(draft_id, None)
