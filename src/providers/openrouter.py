from __future__ import annotations

import os

from .base import OpenAIProvider


class OpenRouter(OpenAIProvider):
    """ Needs OPENROUTER_API_KEY, free models work without credits."""

    name = "openrouter"
    label = "OpenRouter"
    endpoint = "https://openrouter.ai/api/v1/chat/completions"
    model = "meta-llama/llama-3.3-70b-instruct:free"
    supports_vision = True
    requires_key = True

    def __init__(self, api_key: str | None = None) -> None:
        super().__init__(api_key or os.getenv("OPENROUTER_API_KEY"))
        self.vision_model = os.getenv("OPENROUTER_VISION_MODEL") or "google/gemini-2.0-flash-exp:free"


openrouter = OpenRouter()
