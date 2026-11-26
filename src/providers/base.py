from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any

import aiohttp

Message = dict[str, Any]
Messages = list[Message]


class ProviderError(Exception):
    """ Any provider failure, message is safe to log."""


def has_images(messages: Messages) -> bool:
    """ True when any message carries multimodal image parts."""
    for message in messages:
        content = message.get("content")
        if isinstance(content, list) and any(
            isinstance(part, dict) and part.get("type") == "image_url" for part in content
        ):
            return True
    return False


def flatten(content: Any) -> str:
    """ Turns multimodal content into plain text."""
    if isinstance(content, str):
        return content
    return "\n".join(
        part.get("text", "") for part in content or [] if isinstance(part, dict) and part.get("type") == "text"
    )


class BaseProvider:
    """ Shared async interface for every chat provider."""

    name: str = "base"
    label: str = "Base"
    model: str = ""
    timeout: float = 90.0
    supports_stream: bool = False
    supports_vision: bool = False
    requires_key: bool = False

    def ready(self) -> bool:
        """ False means the provider is skipped by the manager."""
        return True

    async def chat(self, messages: Messages, *, model: str | None = None) -> str:
        raise NotImplementedError

    async def stream(self, messages: Messages, *, model: str | None = None) -> AsyncIterator[str]:
        raise NotImplementedError
        yield ""


class OpenAIProvider(BaseProvider):
    """ Provider for endpoints shaped like OpenAI's chat completions."""

    endpoint: str = ""
    headers: dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
        "Content-Type": "application/json",
    }
    supports_stream = True
    vision_model: str | None = None

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key

    def ready(self) -> bool:
        return not self.requires_key or bool(self.api_key)

    def auth(self) -> dict[str, str]:
        if self.api_key:
            return {"Authorization": f"Bearer {self.api_key}"}
        return {}

    def payload(self, messages: Messages, model: str | None, stream: bool) -> dict[str, Any]:
        chosen = model or self.model
        if self.vision_model and has_images(messages):
            chosen = self.vision_model
        return {"model": chosen, "messages": messages, "stream": stream}

    async def chat(self, messages: Messages, *, model: str | None = None) -> str:
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                self.endpoint,
                json=self.payload(messages, model, False),
                headers={**self.headers, **self.auth()},
            ) as response:
                body = await response.text()
                if response.status >= 400:
                    raise ProviderError(f"{self.name}: HTTP {response.status} {body[:160]}")
                try:
                    return json.loads(body)["choices"][0]["message"]["content"]
                except (ValueError, KeyError, IndexError) as exc:
                    raise ProviderError(f"{self.name}: unexpected response") from exc

    async def stream(self, messages: Messages, *, model: str | None = None) -> AsyncIterator[str]:
        timeout = aiohttp.ClientTimeout(total=None, sock_connect=15, sock_read=self.timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                self.endpoint,
                json=self.payload(messages, model, True),
                headers={**self.headers, **self.auth()},
            ) as response:
                if response.status >= 400:
                    raise ProviderError(f"{self.name}: HTTP {response.status}")
                async for raw in response.content:
                    line = raw.decode(errors="ignore").strip()
                    if not line.startswith("data:"):
                        continue
                    data = line[5:].strip()
                    if data == "[DONE]":
                        break
                    try:
                        event = json.loads(data)
                    except ValueError:
                        continue
                    choices = event.get("choices") or [{}]
                    chunk = choices[0].get("delta", {}).get("content")
                    if chunk:
                        yield chunk
