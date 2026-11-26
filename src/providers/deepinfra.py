from __future__ import annotations

import os

from .base import OpenAIProvider


class DeepInfra(OpenAIProvider):
    """ Needs DEEPINFRA_API_KEY, skipped when the key is missing."""

    name = "deepinfra"
    label = "DeepInfra"
    endpoint = "https://api.deepinfra.com/v1/openai/chat/completions"
    model = "meta-llama/Llama-3.3-70B-Instruct"
    supports_vision = True
    requires_key = True

    def __init__(self, api_key: str | None = None) -> None:
        super().__init__(api_key or os.getenv("DEEPINFRA_API_KEY"))
        self.vision_model = os.getenv("DEEPINFRA_VISION_MODEL") or "Qwen/Qwen2.5-VL-72B-Instruct"


deepinfra = DeepInfra()
