from __future__ import annotations

from i18n import i18n
from telegram import inline, pack

LANGUAGE_NAMES = {
    "en": "🇬🇧 English",
    "fa": "🇮🇷 فارسی",
    "ru": "🇷🇺 Русский",
    "tr": "🇹🇷 Türkçe",
    "so": "🇸🇴 Soomaali",
}


def language_rows() -> list[list[tuple[str, str, str]]]:
    buttons = [(LANGUAGE_NAMES.get(name, name.upper()), pack("lang", name), "primary") for name in i18n.languages]
    return [buttons[index : index + 2] for index in range(0, len(buttons), 2)]


def language_menu(t):
    return inline([*language_rows(), [(t("common.back"), pack("menu", "back"), "primary")]])


def main_menu(t):
    return inline(
        [
            [(t("start.menu_chat"), pack("menu", "chat"), "primary"), (t("start.menu_image"), pack("menu", "image"), "success")],
            [(t("start.menu_voice"), pack("menu", "voice"), "success"), (t("start.menu_settings"), pack("menu", "settings"), "primary")],
            [(t("start.menu_sessions"), pack("session", "list"), "primary"), (t("start.menu_history"), pack("menu", "history"), "primary")],
            [(t("start.menu_help"), pack("menu", "help"), "primary"), (t("start.menu_language"), pack("menu", "language"), "primary")],
        ]
    )


def back_menu(t):
    return inline([[(t("common.back"), pack("menu", "back"), "primary")]])


def welcome_text(t, name: str, existing: bool) -> str:
    greeting = t("start.welcome_back" if existing else "start.welcome", name=name)
    return f"{greeting}\n\n{t('start.subtitle')}"
