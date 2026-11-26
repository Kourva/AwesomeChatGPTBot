from __future__ import annotations

import os

import aiohttp

from .base import ProviderError

HEADERS = {"User-Agent": "Mozilla/5.0"}
VOICEPODS = "https://voicepods-stream.vercel.app/api/resemble"
VOICEPODS_HEADERS = {
    "Origin": "https://voicepods-stream.vercel.app",
    "Referer": "https://voicepods-stream.vercel.app/",
}


class TextToSpeech:
    """ Free voice generator, returns mp3 bytes for Telegram voices."""

    name = "streamelements"
    voices = ("Brian", "Emma", "Joanna", "Matthew")

    def __init__(self, voice: str = "Brian", provider: str | None = None) -> None:
        self.voice = voice
        self.provider = provider or os.getenv("TTS_PROVIDER") or "streamelements"

    async def say(self, text: str, *, voice: str | None = None, language: str = "en") -> bytes:
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=timeout, headers=HEADERS) as session:
            if self.provider == "voicepods":
                try:
                    return await self._voicepods(session, text)
                except (ProviderError, aiohttp.ClientError):
                    pass
            try:
                return await self._stream_elements(session, text, voice or self.voice)
            except (ProviderError, aiohttp.ClientError):
                return await self._google(session, text, language)

    async def _stream_elements(self, session: aiohttp.ClientSession, text: str, voice: str) -> bytes:
        params = {"voice": voice, "text": text}
        async with session.get(
            "https://api.streamelements.com/kappa/v2/speech", params=params
        ) as response:
            if response.status >= 400:
                raise ProviderError(f"tts: HTTP {response.status}")
            return await response.read()

    async def _voicepods(self, session: aiohttp.ClientSession, text: str) -> bytes:
        """ Voicepods returns a WAV stream, sometimes with a prepended header."""
        async with session.post(VOICEPODS, json={"query": text}, headers=VOICEPODS_HEADERS) as response:
            if response.status >= 400:
                raise ProviderError(f"tts: HTTP {response.status}")
            data = await response.read()

        start = data.find(b"RIFF")
        if start < 0 or len(data) - start < 1024:
            raise ProviderError("tts: voicepods returned no audio")
        return data[start:]

    async def _google(self, session: aiohttp.ClientSession, text: str, language: str) -> bytes:
        params = {"ie": "UTF-8", "q": text, "tl": language, "client": "tw-ob"}
        async with session.get("https://translate.google.com/translate_tts", params=params) as response:
            if response.status >= 400:
                raise ProviderError(f"tts: HTTP {response.status}")
            return await response.read()


tts = TextToSpeech()
