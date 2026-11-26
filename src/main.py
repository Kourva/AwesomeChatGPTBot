#!/usr/bin/env python3

import asyncio
import sys

from telebot import util

from bot.register import register
from config import global_config
from database import setup
from init import initialize
from logger import logger


async def main() -> None:
    bot = initialize()
    database = await setup(global_config["database"])
    register(bot)
    logger.info(f"Bot is running with ID: {bot.bot_id}")

    try:
        await bot.polling(skip_pending=True, allowed_updates=util.update_types)
    finally:
        await database.close()
        await bot.close_session()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.error("Program interrupted using Ctrl+C")
        sys.exit(0)
