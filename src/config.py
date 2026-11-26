import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()


def _number(value: str | None, default: int = 0) -> int:
    try:
        return int(value or default)
    except ValueError:
        return default


def _database_path() -> str:
    path = os.getenv("DATABASE_PATH") or "src/database/"
    if not path.endswith(".db"):
        path = os.path.join(path, "bot.db")
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    return path


def config() -> dict[str, Any]:
    return {
        "admin_id": _number(os.getenv("ADMIN_ID")),
        "database": _database_path(),
        "default_language": os.getenv("DEFAULT_LANGUAGE") or "en",
        "tts_voice": os.getenv("TTS_VOICE") or "Brian",
        "history_limit": _number(os.getenv("HISTORY_LIMIT"), 20),
    }


global_config = config()
