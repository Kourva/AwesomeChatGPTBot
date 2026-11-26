from __future__ import annotations

import aiohttp

from .base import BaseProvider, Messages, ProviderError, flatten


class Phind(BaseProvider):
    """ Free DeepSeek provider, public JSON route, no key."""

    name = "phind"
    label = "Phind"
    model = "deepseek-v3"
    timeout = 120.0
    endpoint = "https://phindai.org/wp-json/phind/v1/chat"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/137.0 Safari/537.36",
        "Content-Type": "application/json",
    }

    async def chat(self, messages: Messages, *, model: str | None = None) -> str:
        payload = {
            "message": flatten(messages[-1]["content"]),
            "history": [
                {"role": item["role"], "content": flatten(item["content"])}
                for item in messages[:-1]
                if item.get("role") in ("user", "assistant")
            ][-10:],
        }
        timeout = aiohttp.ClientTimeout(total=self.timeout)

        async with aiohttp.ClientSession(timeout=timeout, headers=self.headers) as session:
            async with session.post(self.endpoint, json=payload) as response:
                data = await response.json(content_type=None)
                if response.status >= 400 or data.get("error"):
                    raise ProviderError(f"phind: HTTP {response.status} {data.get('error', '')}")

        text = data.get("response", "")
        if not text:
            raise ProviderError("phind: empty response")
        return text


phind = Phind()
