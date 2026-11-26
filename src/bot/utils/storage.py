from __future__ import annotations

from collections.abc import Callable
from typing import Any

from config import global_config
from database import ProviderSetting, User
from i18n import i18n
from providers import manager


async def get_user(account: Any) -> User:
    """ Returns the stored user, creates it with defaults on first use."""
    user = await User.get(id=account.id)
    if user is not None:
        return user

    language = (account.language_code or "").split("-")[0]
    if language not in i18n.languages:
        language = global_config["default_language"]
    if language not in i18n.languages:
        language = "en"

    user = await User.create(
        id=account.id,
        username=account.username,
        first_name=account.first_name,
        last_name=account.last_name,
        language=language,
    )
    await ProviderSetting.seed(user.id, manager.names())
    return user


def translate(user: User) -> Callable[..., str]:
    return i18n.for_language(user.language or global_config["default_language"])
