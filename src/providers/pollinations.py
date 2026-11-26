from __future__ import annotations

import secrets
from typing import Any
from urllib.parse import quote, urlencode

from .base import Messages, OpenAIProvider


class Pollinations(OpenAIProvider):
    """ Free text and image provider, no key needed."""

    name = "pollinations"
    label = "Pollinations"
    endpoint = "https://text.pollinations.ai/openai"
    model = "openai-fast"
    timeout = 120.0

    def payload(self, messages: Messages, model: str | None, stream: bool) -> dict[str, Any]:
        """# A random seed keeps repeat requests (regenerate) out of the response cache."""
        data = super().payload(messages, model, stream)
        data["seed"] = secrets.randbelow(1_000_000_000)
        return data

    def image(
        self,
        prompt: str,
        *,
        width: int = 1024,
        height: int = 1024,
        seed: int | None = None,
    ) -> str:
        """ Returns an image URL, Telegram fetches it directly."""
        params = {"width": width, "height": height, "nologo": "true"}
        if seed is not None:
            params["seed"] = seed
        return f"https://image.pollinations.ai/prompt/{quote(prompt)}?{urlencode(params)}"


pollinations = Pollinations()
