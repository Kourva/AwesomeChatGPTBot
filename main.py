#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# FreeChatGPT telegram bot
# Developed by Kourva
# Source code: https://github.com/Kourva/AwesomeChatGPTBot


# Libraries
import telebot                        # Bot API Library
import requests                       # Internet requests
import utils                          # Bot Utilities
import json                           # Json function
import os                             # OS functions
from telebot.util import quick_markup # Markup generator
from utils import ChatGPT_Function    # ChatGPT function


# Connect to bot
# Token placed in utils.py file. You can change it with your token
GPTbot = telebot.TeleBot(utils.Token)
print(f"The Bot is online (id: {GPTbot.get_me().id})...")


# Start message handler
@GPTbot.message_handler(commands=["start", "restart"])
def start_command_handler(message: object) -> None:
    """
    Function   to   handle /start  & /restart  command
    Creates account for user and sends welcome message
    """

    # Search for user account that is exist or not
    if (ufile := f"{message.from_user.id}") in os.listdir("Accounts/"):
            
        # Send welcome back message to user
        GPTbot.send_chat_action(
            chat_id=message.chat.id, 
            action="typing"
        )
        GPTbot.reply_to(
            message=message,
            text=f"Welcome Back {message.from_user.first_name}.\nLet's chat! (Use /settings for settings).",
        )

    # Continue if user is new member and create account for user
    else:

        # Send welcome message to new user
        GPTbot.send_chat_action(
            chat_id=message.chat.id, 
            action="typing"
        )
        GPTbot.reply_to(
            message=message,
            text=f"Welcome Dear {message.from_user.first_name}.\nLet's chat! (Use /settings for settings).",
   
        )

        # Initialize user account's files
        os.mkdir(f"Accounts/{ufile}")                   # User account
        open(f"Accounts/{ufile}/chatgpt", "w").close()  # GPT history


# Settings command handler
@GPTbot.message_handler(commands=["settings"])
def gpt_command_handler(message: object) -> None:
    """
    Function       to       handle      settings       command
    Show user chatGPT account information or renew chat status
    """

    # Make reply markup for settings
    Markups = quick_markup(
        {
            "Renew Chat": {
                "callback_data": f"ReNewGpt_{message.from_user.id}"
            },
            "Account Info": {
                "callback_data": f"InfoGpt_{message.from_user.id}"
            },
            "Close": {
                "callback_data": "Close"
            },
        },
        row_width=2,
    )

    # Send GPT menu to user
    GPTbot.send_chat_action(
        chat_id=message.chat.id,
        action="typing"
    )
    GPTbot.reply_to(
        message=message,
        text="Welcome to ChatGPT settings!",
        reply_markup=Markups
    )



# Callback query handler for buttons used in settings
@GPTbot.callback_query_handler(func=lambda call: True)
def callback_query(call: object) -> None:
    """
    This function will handle the inline keyboards callback
    Show    results   and    Answer  the  callback  queries
    """
    
    # Initialize the IDs (User ID), (Chat ID), (Message ID)
    try:uid = call.from_user.id 
    except:pass

    try:cid = call.message.chat.id
    except:pass

    try:mid = call.message.message_id
    except:pass

    
    # Callback handler for chatGPT history renewing
    if call.data.startswith("ReNewGpt_"):

        # Error handling
        try:

            # Get user id from argument
            user_id = call.data.split("_")[1]

            # Delete chat history
            with open(f"Accounts/{user_id}/chatgpt", "w") as d:
                d.write("")

            # Answer query
            GPTbot.answer_callback_query(
                call.id,
                "Your Chat History Deleted!",
                show_alert=True
            )
            # Delete the message (Close)
            GPTbot.delete_message(
                chat_id=cid, 
                message_id=mid
            )

        # Show error message if operation failed
        except:

            # Show error message
            GPTbot.answer_callback_query(
                call.id,
                "Could not do this operation :(",
            )


    # Callback handler for Gpt account information
    elif call.data.startswith("InfoGpt_"):

        # Error handling
        try:

            # Get user id
            user_id = call.data.split("_")[1]

            # Get gpt info
            with open(f"Accounts/{user_id}/chatgpt", "r") as d:
                
                # If history file is empty
                if (datas:=d.read()) == "":
                    
                    # Show message
                    GPTbot.answer_callback_query(
                        call.id,
                        "You don't have any chat history yet :("
                    )
                
                # Continue if there is valid config
                else:
                    
                    # Fetch chat id and last message id
                    chat_id = datas.split("@")[0].strip()
                    mseg_id = datas.split("@")[1].strip()
                    
                    # Show message
                    GPTbot.answer_callback_query(
                        call.id,
                        (
                            f"▋Conversation ID:\n{chat_id}\n\n"
                            f"▋Last Message ID:\n{mseg_id}"
                        ),
                        show_alert=True
                    )

        # Show error message if operation failed
        except:

            # Show error message
            GPTbot.answer_callback_query(
                call.id,
                "Could not do this operation :("
            )


    # Callback handler for Close option
    elif call.data == "Close":


        # Error handling
        try:
            
            # Delete the message (Close)
            GPTbot.delete_message(
                chat_id=cid, 
                message_id=mid
            )

        except:

            # Show error message
            GPTbot.answer_callback_query(
                call.id,
                "Could not do this operation for now :("
            )


# Inline      handler   for      code      command
# Don't forget to enable your bot inline mode from
# your         bot      setting    in   @BotFather 
@GPTbot.inline_handler(lambda query: query.query == "gpt")
def query_text(inline_query: object) -> None:
    """
    Function to handle   inline gpt prompts
    Shows settings for gpt account for user
    """

    # Error handling
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

    # Pass errors (log)
    except Exception as e:
    	print(e)


# Handle user messages
@GPTbot.message_handler(func=lambda message: True)
def handle_messages(message):
    """
    Function     to handle  all  messages  in  bot   (except / commands )
    This     will    handle   user  messages      with        ChatGPT-3.5
    """

    # Avoid        making       mess   for    replying    in       groups
    # Let's say  I   replied message  to bot  in group  and bot  answered
    # If you reply  to my  message bot will also  answer to  your message
    # Because replies are connected, this statement is for  avoiding this
    # Issue    in     groups.  (  Or     maybe     private        chat  )
    if message.reply_to_message and message.reply_to_message.from_user.id == GPTbot.get_me().id:

        # Get user input
        user_input = message.text.strip()

        # Send waiting message
        # Note some characters escaped for parse mode
        GPTbot.send_chat_action(
            chat_id=message.chat.id,
            action="typing"
        )
        gpt_prompt = GPTbot.reply_to(
            message=message,
            text="Bot is thinking\.\.\.",
            parse_mode="MarkdownV2",
        ) 

        # Fetch results from function
        result = ChatGPT_Function(message.from_user.id, user_input)

        # Edit waiting message and answer user message
        GPTbot.edit_message_text(
            chat_id=message.chat.id,
            message_id=gpt_prompt.message_id,
            text=utils.escape_markdown(result),
            parse_mode="MarkdownV2",
        )


    # If chat mode is private (chat in bot)
    elif utils.force_private(message):

        # Gets user input
        user_input = message.text.strip()

        # Send waiting message
        GPTbot.send_chat_action(
            chat_id=message.chat.id,
            action="typing"
        )
        gpt_prompt = GPTbot.reply_to(
            message=message,
            text="Bot is thinking\.\.\.",
            parse_mode="MarkdownV2",
        )

        # Fetch results from function
        result = ChatGPT_Function(message.from_user.id, user_input)

        # Answer user message
        GPTbot.edit_message_text(
            chat_id=message.chat.id,
            message_id=gpt_prompt.message_id,
            text=utils.escape_markdown(result),
            parse_mode="MarkdownV2",
        )


# Connect to  bot in  infinite polling mode
# Make   bot  connection       non     stop
# Skip      old    messages,  don't  update
if __name__ == "__main__":

    # Error handling 
    try:
        GPTbot.infinity_polling(
            skip_pending=True, 
            none_stop=True,
        )

    # Except any error
    except: 
        print("Lost connection!")
