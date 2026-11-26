from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class SafeDict(dict):
    """ Leaves unknown placeholders untouched instead of raising."""

    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


class I18n:
    """ Loads JSON catalogs and translates dotted keys."""

    def __init__(self, directory: str | Path | None = None, default: str = "en") -> None:
        self.directory = Path(directory) if directory else Path(__file__).parent / "locales"
        self.default = default
        self.catalogs: dict[str, dict[str, Any]] = {}

    @property
    def languages(self) -> list[str]:
        return sorted(path.stem for path in self.directory.glob("*.json"))

    def catalog(self, language: str) -> dict[str, Any]:
        if language not in self.catalogs:
            path = self.directory / f"{language}.json"
            self.catalogs[language] = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        return self.catalogs[language]

    def t(self, key: str, language: str | None = None, **values: Any) -> str:
        language = language or self.default
        text = self._lookup(self.catalog(language), key)
        if text is None and language != self.default:
            text = self._lookup(self.catalog(self.default), key)
        if text is None:
            return key

        if isinstance(text, dict):
            text = self._plural(text, values.get("count"))

        return str(text).format_map(SafeDict(values))

    def for_language(self, language: str):
        """ Returns a translate function, handy inside handlers."""
        def translate(key: str, **values: Any) -> str:
            return self.t(key, language, **values)

        return translate

    def _lookup(self, catalog: dict[str, Any], key: str) -> Any:
        value: Any = catalog
        for part in key.split("."):
            if not isinstance(value, dict) or part not in value:
                return None
            value = value[part]
        return value

    def _plural(self, forms: dict[str, str], count: Any) -> str | None:
        if count is None:
            return None
        return forms.get("one") if abs(int(count)) == 1 else forms.get("other") or forms.get("one")


i18n = I18n()
