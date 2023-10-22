<p align="center">
    <img align='left' src="https://github.com/Kourva/AwesomeChatGPTBot/assets/118578799/ef1cfefd-1e58-45d3-8a3a-fa9988a8322e" width=200 height=200/>
    <h2>Free Chat GPT Telegram Bot </h2>
  <p><i>Free ChatGPT-3.5 Telegram Bot with option to remenber chat history and pre-defined roles!</i></p>
  <p><i>Without any <b>API-key</b> from OpenAI and other stuff <b>+</b> Inline bot</i></p>
</p>
<br><br>

# ▋Attention
Bot has been updated and works fine
+ history section added
+ **/history** to get history file in json format
+ **/reset** to reset the chat history
+ **/danmode** to enable/disable DAN mode v10.0 in bot
> Note: History will reset when using /danmode command!!



<br>

# ▋Features
This bot response to every message with ChatGpt prompt (excluding commands)
+ **Inline mode** to get pre-defined *Roles*
+ Can remember history

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
After getting **Token** from **BotFather** replace the Token in `utils.py` in line **7** as follows:
```python
# Bot token to use
Token = "6146793572:AAE7fbH29UPOKzlHlp0YDr9o06o_NdD4DBk"
```
> This is just an example Token. Use yours instead

<br>

# ▋Configure the bot commands
you can set your bot's commands manually or using 'init.py' script
```bash
python init.py
```
> This will set up `/history`, `/start` and `/reset` commands in bot

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
