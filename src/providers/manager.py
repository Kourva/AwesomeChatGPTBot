from __future__ import annotations

import asyncio
import time
from collections.abc import AsyncIterator, Iterable
from dataclasses import dataclass

from .base import BaseProvider, Messages, ProviderError, has_images


@dataclass(slots=True)
class ChatResult:
    text: str
    provider: str
    model: str
    elapsed: float


class ProviderManager:
    """ Tries enabled providers one by one, first valid answer wins."""

    def __init__(self, *providers: BaseProvider) -> None:
        self.providers: dict[str, BaseProvider] = {p.name: p for p in providers}
        self.errors: dict[str, str] = {}

    def register(self, *providers: BaseProvider) -> None:
        for provider in providers:
            self.providers[provider.name] = provider

    def get(self, name: str) -> BaseProvider | None:
        return self.providers.get(name)

    def names(self) -> list[str]:
        return list(self.providers)

    def ready(self, enabled: Iterable[str] | None = None) -> list[BaseProvider]:
        names = list(enabled) if enabled is not None else self.names()
        return [self.providers[n] for n in names if n in self.providers and self.providers[n].ready()]

    def vision_ready(self, enabled: Iterable[str] | None = None) -> bool:
        return any(item.supports_vision for item in self.ready(enabled))

    async def chat(
        self,
        messages: Messages,
        *,
        provider: str | None = None,
        enabled: Iterable[str] | None = None,
        model: str | None = None,
    ) -> ChatResult:
        candidates = self._candidates(provider, enabled, vision=has_images(messages))
        failures: list[str] = []

        for current in candidates:
            started = time.monotonic()
            try:
                text = await current.chat(messages, model=model)
                if not text or not text.strip():
                    raise ProviderError("empty response")
                self.errors.pop(current.name, None)
                return ChatResult(
                    text=text.strip(),
                    provider=current.name,
                    model=model or current.model,
                    elapsed=round(time.monotonic() - started, 2),
                )
            except Exception as exc:
                self.errors[current.name] = str(exc)
                failures.append(f"{current.name}: {exc}")

        raise ProviderError("all providers failed | " + " | ".join(failures))

    async def stream(
        self,
        messages: Messages,
        *,
        provider: str | None = None,
        enabled: Iterable[str] | None = None,
        model: str | None = None,
    ) -> AsyncIterator[str]:
        candidates = self._candidates(provider, enabled, vision=has_images(messages))
        failures: list[str] = []

        for current in candidates:
            if not current.supports_stream:
                continue
            started = False
            try:
                async for chunk in current.stream(messages, model=model):
                    started = True
                    yield chunk
                if started:
                    self.errors.pop(current.name, None)
                    return
            except Exception as exc:
                self.errors[current.name] = str(exc)
                failures.append(f"{current.name}: {exc}")
                if started:
                    raise ProviderError(f"stream broke after start | {exc}") from exc

        # no stream available, fall back to a normal answer
        result = await self.chat(
            messages,
            provider=provider,
            enabled=None if provider else enabled,
            model=model,
        )
        yield result.text

    async def ping(self, names: Iterable[str] | None = None) -> dict[str, bool]:
        """ Sends a tiny prompt to every provider concurrently."""

        async def check(item: BaseProvider) -> tuple[str, bool]:
            try:
                answer = await item.chat([{"role": "user", "content": "Reply with: ok"}])
                return item.name, bool(answer.strip())
            except Exception as exc:
                self.errors[item.name] = str(exc)
                return item.name, False

        targets = self.ready(names)
        results = await asyncio.gather(*(check(item) for item in targets))
        return dict(results)

    def _candidates(
        self,
        provider: str | None,
        enabled: Iterable[str] | None,
        *,
        vision: bool = False,
    ) -> list[BaseProvider]:
        if provider:
            item = self.providers.get(provider)
            if item is None:
                raise ProviderError(f"unknown provider: {provider}")
            if not item.ready():
                raise ProviderError(f"provider not configured: {provider}")
            candidates = [item]
        else:
            candidates = self.ready(enabled)
            if not candidates:
                raise ProviderError("no provider available")

        if vision:
            candidates = [item for item in candidates if item.supports_vision]
            if not candidates:
                raise ProviderError("no vision provider available")
        return candidates


manager = ProviderManager()
