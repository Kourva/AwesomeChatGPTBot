import os
import re

from dotenv import load_dotenv
from telebot import asyncio_helper
from telebot.async_telebot import AsyncTeleBot

load_dotenv()

PROXY_PATTERN = re.compile(r"https?://[^\s/]+(?:/[^\s]*)?")


def initialize() -> AsyncTeleBot:
    proxy_url = os.getenv("PROXY_URL") or ""
    proxy_secret = os.getenv("PROXY_SECRET") or ""

    if PROXY_PATTERN.fullmatch(proxy_url) and len(proxy_secret) == 64:
        asyncio_helper.API_URL = f"{proxy_url}/bot{{0}}/{{1}}?key={proxy_secret}"
        asyncio_helper.FILE_URL = f"{proxy_url}/file/bot{{0}}/{{1}}?key={proxy_secret}"

    token = os.getenv("BOT_TOKEN") or ""
    if ":" not in token:
        raise KeyError("No token provided")

    return AsyncTeleBot(token=token, validate_token=True)
