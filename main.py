#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# FreeChatGPT telegram bot
# Developed by Kourva
# Source code: https://github.com/Kourva/AwesomeChatGPTBot


# Resources
import telebot
import requests
import utils
import json
import os
from datetime import datetime
from telebot import types, util
from telebot.util import quick_markup
from utils import ChatGPT_Function


# Connect to bot
# Token placed in utils.py file. You can change it with your token
GPTbot = telebot.TeleBot(utils.Token)
print(f"The Bot is online (id: {GPTbot.get_me().id})...")


# Start message handler
@GPTbot.message_handler(commands=["start"])
def start_command_handler(message: callable) -> None:
    """
    Function to handle /start command

    Parameter: 
        Message object

    Returns: 
        None
    """

    # User ID
    user_id = message.from_user.id

    # Check if the user account exists
    if os.path.exists(f"Accounts/{user_id}"):
            
        # Send welcome back message to existing user
        GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
        GPTbot.reply_to(
            message=message,
            text=f"Welcome Back {message.from_user.first_name}.\nLet's chat!\n\nCommands usage:\n/history: Get history in json format.\n/reset: Reset the chat",
        )

    else:

        # Create user account for new member
        os.mkdir(f"Accounts/{user_id}")
        with open(f'Accounts/{user_id}/history.json', 'w') as file:
            json.dump([], file)

        # Send welcome back message to existing user
        GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
        GPTbot.reply_to(
            message=message,
            text=f"Welcome Dear {message.from_user.first_name}.\nLet's chat!\n\nCommands usage:\n/history: Get history in json format.\n/reset: Reset the chat",
        )


# History command handler
@GPTbot.message_handler(commands=["history"])
def gpt_command_handler(message: callable) -> None:
    """
    Function to handle /history command

    Parameter: 
        Message object

    Returns: 
        None
    """

    # User ID
    user_id = message.from_user.id

    # Send Wait prompt 
    GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
    prompt = GPTbot.reply_to(
        message=message,
        text="Sending your chat history..."
    )

    # Send user's history
    with open(f"Accounts/{user_id}/history.json", "rb") as file:
    
        GPTbot.send_chat_action(chat_id=message.chat.id, action="upload_document")
        GPTbot.send_document(
            chat_id=message.chat.id,
            document=file,
            caption=f"GPT history. {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            reply_to_message_id=prompt.message_id,
            visible_file_name="GPT History"
        )

    # Edit previous prompt
    prompt = GPTbot.edit_message_text(
        chat_id=message.chat.id,
        message_id=prompt.message_id,
        text="Here is your chat history."
    )


# Reset command handler
@GPTbot.message_handler(commands=["reset"])
def gpt_command_handler(message: callable) -> None:
    """
    Function to handle /history command

    Parameter: 
        Message object

    Returns: 
        None
    """

    # User ID
    user_id = message.from_user.id

    # Clear history
    with open(f'Accounts/{user_id}/history.json', 'w') as file:
        json.dump([], file)

    # Send message to user
    GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
    prompt = GPTbot.reply_to(
        message=message,
        text="Your history cleared."
    )


# Inline handler for GPT prompts
# Don't forget to enable inline mode from @BotFather 
@GPTbot.inline_handler(lambda query: query.query == "prompt")
def query_text(inline_query: callable) -> None:
    """
    Function to handle prompt inline

    Parameter: 
        Inline Query Object

    Returns: 
        None
    """

    try:
        # Create results list
        results = []

        # Convert the dictionary to a list of tuples
        sorted_tuples = sorted(utils.GPT_Prompts.items())

        # Create a new dictionary from the sorted list of tuples
        sorted_dict = {key: value for key, value in sorted_tuples}

        # Add items to results
        for Index, (Title, Prompt) in enumerate(sorted_dict.items(), start=1):
            results.append(
                types.InlineQueryResultArticle(
                    Index,
                    Title,
                    types.InputTextMessageContent(Prompt),
                    description=f"Bot will act as {Title}."
                )
            )

        # Show all results
        GPTbot.answer_inline_query(
            inline_query.id, results
        )

    # Pass errors
    except Exception as e:
        print(e)


# Handle text messages
@GPTbot.message_handler(content_types=["text"])
def handle_messages(message: callable) -> None:
    """
    Function to handle all text messages
     
    Parameter: 
        Message object

    Returns: 
        None
    """

    # User ID
    user_id = message.from_user.id

    # Gets user input
    user_prompt = message.text.strip()

    # Avoid making mess for replying in groups
    if message.reply_to_message and message.reply_to_message.from_user.id == GPTbot.get_me().id:

        # Send waiting message
        GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
        gpt_prompt = GPTbot.reply_to(
            message=message,
            text="Bot is thinking\.\.\.",
            parse_mode="MarkdownV2",
        ) 

        # Fetch results from function
        result = ChatGPT_Function(user_id, user_prompt)

        # Edit waiting message and answer user message
        GPTbot.edit_message_text(
            chat_id=message.chat.id,
            message_id=gpt_prompt.message_id,
            text=utils.escape_markdown(result),
            parse_mode="MarkdownV2",
        )


    # Handle private chat
    elif utils.force_private(message):

        # Send waiting message
        GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
        gpt_prompt = GPTbot.reply_to(
            message=message,
            text="Bot is thinking\.\.\.",
            parse_mode="MarkdownV2",
        )

        # Fetch results from function
        result = ChatGPT_Function(user_id, user_prompt)

        # Answer user message
        GPTbot.edit_message_text(
            chat_id=message.chat.id,
            message_id=gpt_prompt.message_id,
            text=utils.escape_markdown(result),
            parse_mode="MarkdownV2",
        )


# Connect to bot
if __name__ == "__main__":
    try:
        GPTbot.infinity_polling(skip_pending=True, none_stop=True)
    except: 
        print("Lost connection!")
