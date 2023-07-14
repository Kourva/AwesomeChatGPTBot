<h1 align="center">
    <img align='left' src="https://github.com/Kourva/AwesomeChatGPTBot/assets/118578799/ef1cfefd-1e58-45d3-8a3a-fa9988a8322e" width=200 height=200/>
    <h2>Free Chat GPT Telegram Bot </h2>
  <p><i>Free ChatGPT-3.5 Telegram Bot with option to remenber chat history and pre-defined roles!</i></p>
  <p><i>Without any <b>API-key</b> from OpenAI and other stuff <b>+</b> Inline bot</i></p>
</h1>
<br><br>

# ▋Attention (Fixed)
The API used by bot is down temporary and most of alternative chats are down also.<br>
So i updated the api and used another one that have some good and bad points!<br>
+ No Chat history and Message id (bot still can remember but IDK how it works!)
+ Has 6 models **GPT3**, **GPT4**, **Sage**, **Claude** ...

**Problem fixed but you can also use alternative bot!** <br>
**To use new API you need to tun `bot.py` instead of `main.py`**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Libraries
import requests  # Make requests


# MultiChat function
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
```
**Alternativly you can use** `bot.py` **Temporary untill this issue being solved**.

<br>

# ▋Features
This bot response to every message with ChatGpt prompt (excluding commands)
+ **/Settings** command to manage your account
+ **Inline mode** to get pre-defined *Roles*


and the best part is unlike other websites this bot saves the `Conversation-ID` and `Last message-ID` to keep remembering last conversation. so it can remember the chat. **even after 1 day!**

<br>

# ▋Clone Repository
To get started, first you need to **clone** this repository from github into your machine:
```bash
git clone https://github.com/Kourva/AwesomeChatGPTBot
```
and if you dont have git you can install it from your package manager!

<br>

# ▋Install Requirements
Then you have to install requirements before running bot
1. Navigate to bot directory
2. Install requirements using pip
```bash
cd AwesomeChatGPTBot
```
```bash
pip install -r requirements.txt
```
This will install **pyTelegamBotAPI** and **Requests** for you

<br>

# ▋Config your token
Now you have to get create bot from [BotFather](https://t.me/BotFather) **(If you don't have)** and take your **Token** to starts working with your bot.<br>
After getting **Token** from **BotFather** replace the Token in `utils.py` in line **10** as follows:
```python
# Bot token to use
Token = "6146793572:AAE7fbH29UPOKzlHlp0YDr9o06o_NdD4DBk"
```
> This is just an example Token. Use yours instead

<br>

# ▋Launch the bot
Now you are ready to launch your bot in polling mode inside your terminal using python
```bash
python main.py
```
You can also use **proxychains** to run your bot via **Tor** proxy
```bash
proxycahins python main.py
```
Or in quiet mode
```bash
proxychains -q python main.py
```
To install proxychains install `proxychains-ng` and then edit the config file in `/etc/proxychains.conf`.<br>
In config file comment the `strict_chain` and un-comment `dynamic_chain` and its ready to use.
<br>

# ▋TOR new IP address
If you got any denied requests that blocked your Ip address, you can renew your IP
```bash
sudo killall -HUP tor
```

<br>

# ▋Bot Inline Mode
Don't forget to enable **Inline Mode** in your bot.<br>
See documentation here: https://core.telegram.org/bots/api#inline-mode
