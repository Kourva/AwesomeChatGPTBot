#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import utils
import telebot
import requests
from telebot import types, util

# Connect to bot
# Token placed in utils.py file. You can change it with your token
GPTbot = telebot.TeleBot(utils.Token)
print(f"The Bot is online (id: {GPTbot.get_me().id}) \33[0;31m[DEVELOPER MODE]\33[m...")

# Set bot commands
print("[!] Configuring bot commands...")
GPTbot.set_my_commands(
    commands=[
        types.BotCommand(
            command="start",
            description="Start the bot"
        ),
        types.BotCommand(
            command="history",
            description="Get your chat history"
        ),
        types.BotCommand(
            command="reset",
            description="Reset you chat history"
        ),
        types.BotCommand(
            command="danmode",
            description="Enable/Disable DAN mode v 10.0"
        )
    ]
)
print("[!] Commands successfully configured.\n[!] Run main.py")
