from __future__ import annotations

import re

SPECIAL = set("_*[]()~`>#+-=|{}.!\\")
CODE = re.compile(r"```[\s\S]*?```|`[^`\n]+`")


def _plain(text: str) -> str:
    return "".join("\\" + char if char in SPECIAL else char for char in text)


def escape(text: str) -> str:
    """ Escapes text for MarkdownV2."""
    parts: list[str] = []
    position = 0

    for match in CODE.finditer(text):
        parts.append(_plain(text[position : match.start()]))
        parts.append(match.group(0))
        position = match.end()

    parts.append(_plain(text[position:]))
    return "".join(parts)


def bold(text: str) -> str:
    return f"*{escape(text)}*"


def italic(text: str) -> str:
    return f"_{escape(text)}_"


def strike(text: str) -> str:
    return f"~{escape(text)}~"


def spoiler(text: str) -> str:
    return f"||{escape(text)}||"


def quote(text: str) -> str:
    return ">" + escape(text).replace("\n", "\n>")


def code(text: str) -> str:
    return "`" + text.replace("\\", "\\\\").replace("`", "\\`") + "`"


def pre(text: str, language: str = "") -> str:
    body = text.replace("\\", "\\\\").replace("```", "\\`\\`\\`")
    return f"```{language}\n{body}\n```"


def link(text: str, url: str) -> str:
    safe_url = url.replace("\\", "\\\\").replace(")", "\\)")
    return f"[{escape(text)}]({safe_url})"
