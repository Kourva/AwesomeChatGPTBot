#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# FreeChatGPT telegram bot
# Developed by Kourva
# Source code: https://github.com/Kourva/AwesomeChatGPTBot

# Standard library imports
import json
import os
from datetime import datetime
from typing import (
    Any, Dict, List, Tuple, Optional, 
    ClassVar, NoReturn, Callable
)

# Related third party imports
import telebot
import requests
from telebot import types, util
from telebot.util import quick_markup, extract_arguments

# Local application/library specific imports
import utils
import titles
from utils import chat_function
from Providers.deepinfra import deep_infra_chat
from Providers.fstha import fstha_chat_gpt
from Providers.onlinegpt import online_gpt_chat
from Providers.fakeopen import fakeopen_chat

# Initialize the bot with 'TOKEN' defined in utils.py file.
try:
    GPTbot: ClassVar[Any] = telebot.TeleBot(utils.TOKEN)
    print(f"\33[0;32m[*] The Bot is online (bot id: {GPTbot.get_me().id})\33[m...")

# Handle invalid token exception
except telebot.apihelper.ApiTelegramException as ue:
    if "Unauthorized" in ue.description:
        raise SystemExit(
            "Unauthorized Error!\n"
            "  * Your Token is invalid! Use valid one."
        )

# Handle SSL error exception
except requests.exceptions.SSLError:
    raise SystemExit(
        "Maximum number of retries exceeded!\n"
        "  * Check the SSL configuration on the server and ensure it's correct.\n"
        "  * Simply try running the bot again!"
        "  * Ensure that the date and time on your system are correct, as SSL/TLS uses timestamps to validate certificates.\n"
    )

# Handle connection error exception
except requests.exceptions.ConnectionError:
    raise SystemExit(
        "Connection Error!\n"
        "  * Try again with VPN or proxy.\n"
    )

# Handle other exceptions
except Exception as e:
    raise SystemExit(
        f"Unexpected Error!\n  {e}"
    )


# Command handler for 'start' command
@GPTbot.message_handler(commands=["start"])
def start_command_handler(message: ClassVar[Any]) -> NoReturn:
    """
    Function to handle /start command

    Parameter:
        Message object

    Returns:
        None
    """
    # Get user information from message
    user: ClassVar[str, int] = utils.User(message.from_user)

    # Check if /start command pressed normally or not.
    if not (arg:=extract_arguments(message.text)):
        # Check user account path and Create account for new user
        if not os.path.exists(f"Accounts/{user.id}"):
            utils.create_user_account(user.id)
            
            # Send welcome back message to existing user
            GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
            GPTbot.reply_to(
                message=message,
                text=titles.welcome_1.format(user.get_name)
            )

        else:
            # Send welcome back message to existing user
            GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
            GPTbot.reply_to(
                message=message,
                text=titles.welcome_2.format(user.get_name)
            )
    
    # Check if /start command pressed with create command.
    elif arg == "create":
        # Make account for user
        if not os.path.exists(f"Accounts/{user.id}"):
            # Make user account and send welcome message to user
            utils.create_user_account(user.id)
            GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
            GPTbot.reply_to(
                message=message,
                text=titles.welcome_3.format(user.get_name)
            )
        
        # Skip if account is already created
        else:
            # Send welcome message to user
            GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
            GPTbot.reply_to(
                message=message,
                text=titles.welcome_4.format(user.get_name)
            )


# Command handler for 'ping' command
@GPTbot.message_handler(func=lambda x: x.chat.type == "private", commands=["ping"])
def ping_command_handler(message: ClassVar[Any]) -> NoReturn:
    """
    Function to ping all available providers to see status of them

    Parameter:
        Message object

    Returns:
        None
    """
    # Send waiting prompt to user
    GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
    prompt = GPTbot.reply_to(
        message=message,
        text="Getting status! Please wait...",
    ) 

    # Make status mapping for providers
    status_mapping = {
        "deep_infra_chat": "Offline",
        "fstha_chat_gpt": "Offline",
        "online_gpt_chat": "Offline",
        "fakeopen_chat": "Offline"
    }
    # Check providers availability
    for provider in [deep_infra_chat, fstha_chat_gpt, online_gpt_chat, fakeopen_chat]:
        if provider([{"role": "user", "content": "Hi"}]):
            status_mapping[provider.__name__] = "Online"

    # Update waiting prompt and replace status text
    else:
        GPTbot.edit_message_text(
            chat_id=message.chat.id,
            message_id=prompt.message_id,
            text=(
                f"*Status for available providers*:\n\n"
                f"_Deepinfra AI_ (LLAMA 70b):\nstatus -> *{status_mapping['deep_infra_chat']}*\n\n"
                f"_Fstha GPT_ (GPT 3.5 Turbo):\nstatus -> *{status_mapping['fstha_chat_gpt']}*\n\n"
                f"_Online GPT_ (GPT 3.5 Turbo):\nstatus -> *{status_mapping['online_gpt_chat']}*\n\n"
                f"_Fakeopen AI_ (GPT 3.5 Turbo):\nstatus -> *{status_mapping['fakeopen_chat']}*"
            ),
            parse_mode="Markdown"
        )



# Message handler for 'history' command
@GPTbot.message_handler(func=lambda x: x.chat.type == "private", commands=["history"])
def history_command_handler(message: ClassVar[Any]) -> NoReturn:
    """
    Function to handle /history command. This will send users's
    history from first message until last conversation.

    Parameter: 
        Message object

    Returns: 
        None
    """
    try:
        # Get user information from message
        user: ClassVar[str, int] = utils.User(message.from_user)

        # Send user's history
        with open(f"Accounts/{user.id}/history.json", "rb") as file:
            GPTbot.send_chat_action(chat_id=message.chat.id, action="upload_document")
            GPTbot.send_document(
                chat_id=message.chat.id,
                document=file,
                caption=f"Chat GPT history.\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                reply_to_message_id=message.message_id,
                visible_file_name="History (Json)"
            )

    # Raise error if user account not found
    except FileNotFoundError:
        GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
        GPTbot.reply_to(
            message=message,
            text=titles.no_account_warn.format(user.get_name, GPTbot.get_me().username),
            disable_web_page_preview=True
        )
        

# Message handler for 'reset' command
@GPTbot.message_handler(func=lambda x: x.chat.type == "private", commands=["reset"])
def reset_command_handler(message: ClassVar[Any]) -> NoReturn:
    """
    Function to handle /reset command. this command will delete all
    history and make history file empty.

    Parameter: 
        Message object

    Returns: 
        None
    """
    try:
        # Get user information from message
        user: ClassVar[str, int] = utils.User(message.from_user)

        # Clear history
        with open(f"Accounts/{user.id}/history.json", "w") as file:
            json.dump([], file)

        # Send message to user
        GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
        GPTbot.reply_to(
            message=message,
            text=titles.history_cleared.format(user.get_name)
        )

    # Raise error if user account not found
    except FileNotFoundError:
        GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
        GPTbot.reply_to(
            message=message,
            text=titles.no_account_warn.format(user.get_name, GPTbot.get_me().username),
            disable_web_page_preview=True
        )


# Message handle for 'danmode' command
@GPTbot.message_handler(func=lambda x: x.chat.type == "private", commands=["danmode"])
def dan_mode_command_handler(message: ClassVar[Any]) -> NoReturn:
    """
    Function to handle /danmode command. this will enable/disable DAN mode.
    DAN -> Do Anything Now

    Parameter: 
        Message object

    Returns: 
        None
    """
    try:
        # Get user information from message
        user: ClassVar[str, int] = utils.User(message.from_user)
        file_path: int = f"Accounts/{user.id}/history.json"

        # Read history and handle Dan mode
        with open(file_path, "r") as file:
            history: List[Dict[str, Any]] = json.load(file)

        # Add / Remove Dan mode from history
        system_role_exists: bool = any(item.get("role") == "system" for item in history)

        if system_role_exists:
            # Remove system role from history
            temp: List[Dict[str, str]] = [
                item for item in history if item.get("role") != "system"
            ]
            with open(file_path, "w") as file:
                json.dump(temp, file, indent=4)

            GPTbot.reply_to(
                message=message,
                text=titles.dan_mode_disabled,
                parse_mode="Markdown"
            )
        else:
            # Add 'Dan mode' role to history
            history: List[Dict[str, str]] = [
                {"role": "system", "content": utils.DAN_PROMPT}
            ]
            GPTbot.reply_to(
                message=message,
                text=titles.dan_mode_enabled,
                parse_mode="Markdown"
            )
            with open(file_path, "w") as file:
                json.dump(history, file, indent=4)

    # Raise error if user account not found
    except FileNotFoundError:
        GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
        GPTbot.reply_to(
            message=message,
            text=titles.no_account_warn.format(user.get_name, GPTbot.get_me().username),
            disable_web_page_preview=True
        )


# Message handler for 'help' command
@GPTbot.message_handler(func=lambda x: x.chat.type == "private", commands=["help"])
def help_command_handler(message: ClassVar[Any]) -> NoReturn:
    """
    Function to handle /help command. this will show help and usage to user.

    Parameter: 
        Message object

    Returns: 
        None
    """
    # Send help message to user
    GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
    GPTbot.reply_to(
        message=message,
        text=titles.help_message.format(GPTbot.get_me().username),
        parse_mode="Markdown"
    )


# Message handler for 'feature' command
@GPTbot.message_handler(func=lambda x: x.chat.type == "private", commands=["features"])
def feature_command_handler(message: ClassVar[Any]) -> NoReturn:
    """
    Function to handle /feature command. this will show features to user.
    Such as changes in bot.

    Parameter: 
        Message object

    Returns: 
        None
    """
    # Send feature changes to user
    GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
    GPTbot.reply_to(
        message=message,
        text=titles.features,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )


# Message handler for 'chat' command
@GPTbot.message_handler(commands=["chat"])
def chat_command_handler(message: ClassVar[Any]) -> NoReturn:
    """
    Function to handle /chat command, this command is used to chat
    with bot in groups, to avoid making mess in replies and reactions 
    to bot's response, bot will only answer questions that starts with /chat

    Parameter: 
        Message object

    Returns: 
        None
    """
    try:
        # Get user information from message
        user: ClassVar[str, int] = utils.User(message.from_user)
        user_prompt: str = extract_arguments(message.text)

        # Send usage if user just sent '/chat' without prompt
        if not user_prompt:
            GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
            GPTbot.reply_to(
                message=message,
                text=titles.chat_help.format(user.get_name),
                parse_mode="Markdown"
            )
            return

        # Send waiting message
        GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
        gpt_prompt: ClassVar[Any] = GPTbot.reply_to(
            message=message,
            text=titles.response_prompt
        )

        # Making re-generate inline button
        Markups: ClassVar[Any] = quick_markup({
            f"Re-Generate": {
                "callback_data": f"Re-Generate"
            }
        })

        # Fetch results from function
        result: str = chat_function(user.id, user_prompt) or titles.response_error

        # Answer user message
        GPTbot.edit_message_text(
            chat_id=message.chat.id,
            message_id=gpt_prompt.message_id,
            text=utils.escape_markdown(result),
            parse_mode="MarkdownV2",
            reply_markup=Markups
        )

    # Raise error if user account not found
    except FileNotFoundError:
        GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
        GPTbot.reply_to(
            message=message,
            text=titles.no_account_warn.format(user.get_name, GPTbot.get_me().username),
            disable_web_page_preview=True
        )

    # Log exception's message on failure
    except Exception as ex:
        print(str(ex))
        

# Inline handler to handle 'roles' inline query
@GPTbot.inline_handler(lambda query: query.query == "roles")
def inline_query_text_handler(inline_query: ClassVar[Any]) -> NoReturn:
    """
    Function to handle inline roles. this inline handler will show
    all available prompts in bot

    Parameter:
        Inline Query Object

    Returns:
        None
    """
    try:
        # Create results list
        results: List = []

        # Convert the dictionary to a list of tuples
        sorted_tuples: Tuple[str] = sorted(utils.GPT_PROMPTS.items())

        # Create a new dictionary from the sorted list of tuples
        sorted_dict: Dict[str, str] = {key: value for key, value in sorted_tuples}

        # Add items to results
        for Index, (Title, Prompt) in enumerate(sorted_dict.items(), start=1):
            results.append(
                types.InlineQueryResultArticle(
                    Index,
                    Title,
                    types.InputTextMessageContent(Prompt),
                    description=f"Bot will act as {Title}..."
                )
            )
        # Show all results
        GPTbot.answer_inline_query(
            inline_query.id, results
        )

    # Log error message on failure
    except Exception as e:
        print(e)


# Message handler for text content in all chat types (for text conversation)
@GPTbot.message_handler(content_types=["text"])
def handle_messages(message: ClassVar[Any]) -> None:
    """
    Function to handle text messages in chats
     
    Parameter: 
        Message object

    Returns:
        None
    """

    try:
        # Get user information from message
        user: ClassVar[str, int] = utils.User(message.from_user)
        user_prompt: str = message.text.strip()

        # Send waiting prompt
        GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
        gpt_prompt : ClassVar[Any] = GPTbot.reply_to(
            message=message,
            text=titles.response_prompt
        )

        # Making re-generate inline button
        Markups: ClassVar[Any] = quick_markup({
            "Re-Generate": {
                "callback_data": f"Re-Generate"
            }
        })

        # Fetch results from function
        result: str = chat_function(user.id, user_prompt) or titles.response_error

        # Answer user message
        GPTbot.edit_message_text(
            chat_id=message.chat.id,
            message_id=gpt_prompt.message_id,
            text=utils.escape_markdown(result),
            parse_mode="MarkdownV2",
            reply_markup=Markups
        )

    # Raise error if user account not found
    except FileNotFoundError:
        GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
        GPTbot.reply_to(
            message=message,
            text=titles.no_account_warn.format(user.get_name, GPTbot.get_me().username),
            disable_web_page_preview=True
        )


# Callback query handler for re-generating message
@GPTbot.callback_query_handler(func=lambda call:call.data == "Re-Generate")
def re_generate_callback_handler(call: ClassVar[Any]) -> NoReturn:
    # Get chatID and messageID
    chat_id: str = call.message.chat.id
    message_id: str = call.message.message_id

    # Get the content of last replied message
    user_prompt: str = call.message.reply_to_message.text

    try:
        # Remove /chat prefix if exist in message
        if user_prompt.startswith("/chat "):
            user_prompt = user_prompt.replace("/chat ", "")

        # Get user information from message
        user: ClassVar[str, int] = utils.User(call.from_user)

        # Replace waiting prompt with message text
        GPTbot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=titles.response_prompt,
            reply_markup=None
        )

        # Making re-generate inline button
        Markups: ClassVar[Any] = quick_markup({
            "Re-Generate": {
                "callback_data": f"Re-Generate"
            }
        })

        # Fetch results from function
        result: str = chat_function(user.id, user_prompt) or titles.response_error

        # Answer user message
        GPTbot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=utils.escape_markdown(result),
            parse_mode="Markdownv2",
            reply_markup=Markups
        )

    # Raise error if user account not found
    except FileNotFoundError:
        GPTbot.send_chat_action(chat_id=message.chat.id, action="typing")
        GPTbot.reply_to(
            message=message,
            text=titles.no_account_warn.format(user.get_name, GPTbot.get_me().username),
            disable_web_page_preview=True
        )


# Connect to bot
if __name__ == "__main__":
    try:
        GPTbot.infinity_polling(skip_pending=True, none_stop=True)
    except requests.exceptions.ReadTimeout:
        raise SystemExit(
            "Temporary Connection Error!\n"
            "  * Connecting again..."
        )    

    except telebot.apihelper.ApiTelegramException as ce:
        if "Conflict" in ce.description:
            raise SystemExit(
                "Conflict Error: Another bot is running behind!\n"
                "  * Make sure only one bot instance is running."
            )
        
    except Exception as e: 
        raise SystemExit(
            f"Unexpected Error!\n  {e}"
        )
