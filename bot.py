#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# FreeChatGPT telegram bot (Alternative way)
# Developed by Kourva
# Source code: https://github.com/Kourva/AwesomeChatGPTBot


# Libraries
import telebot                        # Bot API Library
import requests                       # Internet requests
import json                           # Json function
import utils                          # Bot utilities
import os                             # OS functions
from telebot.util import quick_markup # Markup generator


# Chat GPT function
def MultiChat(userid, prompt):
    
    # Open user account to select model
    try:
        with open(f"Accounts/{userid}/chat", "r") as c:
            model = c.read().strip()
    except FileNotFoundError:
        model = "beaver"

    # Set target api
    target_api = "https://1.b88.asia/api/chat-process"
    
    # Set payload
    data = {
        "prompt": prompt,
        "options": {},
        "systemMessage": "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown.",
        "temperature": 0.8,
        "top_p": 1,
        "model": model
    }

    try:
        # Send request and decode the response
        response = requests.post(target_api, json=data).content

        # Return final answer
        return response.decode("utf-8")
    
    # Except error
    except Exception as e:
        print(e) # Log

        # Return error message
        return "An error occurred"


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
            text=f"Welcome Back {message.from_user.first_name}.\nLet's chat! (Use /chat for settings).",
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
            text=f"Welcome Dear {message.from_user.first_name}.\nLet's chat! (Use /chat for settings).",
   
        )

        # Initialize user account's files
        os.mkdir(f"Accounts/{ufile}")                  # User account
        with open(f"Accounts/{ufile}/chat", "w") as d: # GPT history
            d.write("beaver")  


# Settings command handler
@GPTbot.message_handler(commands=["chat"])
def gpt_command_handler(message: object) -> None:
    """
    Function       to       handle      settings       command
    Show user chatGPT account information or select chat model
    """

    # Make reply markup for settings
    Markups = quick_markup(
    {
        "chat GPT 4": {"callback_data": f"SetModel_{message.from_user.id}_beaver"},
        "chat GPT 3": {"callback_data": f"SetModel_{message.from_user.id}_chinchilla"},
        "chat Sage": {"callback_data": f"SetModel_{message.from_user.id}_capybara"},
        "Claude 100k": {"callback_data": f"SetModel_{message.from_user.id}_a2_100k"},
        "Claude +": {"callback_data": f"SetModel_{message.from_user.id}_a2_2"},
        "Claude instant": {"callback_data": f"SetModel_{message.from_user.id}_a2"},
        "Info": {"callback_data": f"InfoChat_{message.from_user.id}"},
        "Close": {"callback_data": "Close"},
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
        text="Welcome! Please feel free to choose a model to apply, or if you're curious, you can also check the details of the model you're currently using.",
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


    # Callback handler for Model changer
    if call.data.startswith("SetModel_"):

        # Error handling
        try:
    
            # Fetch model and User id
            userid = call.data.split("_")[1]
            model = "_".join(call.data.split("_")[2:])

            # Get current model
            with open(f"Accounts/{userid}/chat", 'r') as c:
                curent_model = c.read().strip()

            # Edit user account
            with open(f"Accounts/{userid}/chat", "w") as c:
                c.write(model.strip())

            # Models
            models = {
                "beaver": "Chat GPT 4",
                "a2_100k": "Claude 100k",
                "a2_2": "Claude +",
                "a2": "Claude instant",
                "capybara": "Sage",
                "chinchilla": "Chat GPT 3"
            }


            # Answer callback
            GPTbot.answer_callback_query(
                call.id, 
                "The chat model has been updated successfully.\n\n▋Old model: {old}\n▋New model: {new}".format(old=models[curent_model], new=models[model]),
                show_alert=True
            )


        except Exception as e:
            print(e)

            # Show error message
            GPTbot.answer_callback_query(
                call.id, 
                "Apologies, operation unavailable. Please try again later :("
            )


    # Callback handler for Chat info
    elif call.data.startswith("InfoChat_"):

        # Error handling
        try:

            # Fetch user_id
            userid = call.data.split("_")[1]

            # Get model
            with open(f"Accounts/{userid}/chat", 'r') as c:
                model = c.read().strip()
 
            # Models
            models = {
                "beaver": "Chat GPT 4",
                "a2_100k": "Claude 100k",
                "a2_2": "Claude +",
                "a2": "Claude instant",
                "capybara": "Sage",
                "chinchilla": "Chat GPT 3"
            }


            # Show current model
            GPTbot.answer_callback_query(
                call.id, 
                "You are now interacting with the {model}. Please acquaint yourself with its features and functionalities.".format(model=models[model]),
                show_alert=True
            )

        except Exception as e:
            print(e)
            
            # Show error message
            GPTbot.answer_callback_query(
                call.id, 
                "Apologies, operation unavailable. Please try again later :("
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
                "Apologies, operation unavailable. Please try again later :("
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
        result = MultiChat(message.from_user.id, user_input)

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
        result = MultiChat(message.from_user.id, user_input)

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
