<p align="center">
    <img align='left' src="https://github.com/Kourva/AwesomeChatGPTBot/assets/118578799/ef1cfefd-1e58-45d3-8a3a-fa9988a8322e" width=200 height=200/>
    <h2>Free Chat GPT Telegram Bot </h2>
  <p><i>Free ChatGPT-3.5 Telegram Bot with option to remenber chat history and pre-defined roles!</i></p>
  <p><i>Without any <b>API-key</b> from OpenAI and other stuff <b>+</b> Inline bot</i></p>
</p>
<br><br>

# ▋Change Log
Here are the latest additions:
1. **[Nov 13, 2023] PEP8 fixes:** Fixed some PEP8 issues.<br>
2. **[Nov 13, 2023] Extra commands:** Added `help`, `features` and `chat` commands.<br>
3. **[Nov 13, 2023] MarkdownV2:** Added converter to convert regular markdown to Markdown V2.<br>
4. **[Nov 13, 2023] History management**: Added utilities to check history and fix it when it got broken.<br>
5. **[Nov 13, 2023] Improved chat handler**: Users now requied to use /chat in groups to chat with bot.<bt>
```
/chat hi
```
> This will avoid mess in replies and even reactions to bot's responses

# ▋Upcoming Features
1. **Smart reply**: Reply to user's message to process them with GPT.<br>
2. **Code Generator**: Use code generator to generate functions in many languages.<br>
3. **Image generator**: Use AI to generate images from prompt.

<br>

# ▋Old Changes
> + history section added
> + **/history** to get history file in json format
> + **/reset** to reset the chat history
> + **/danmode** to enable/disable DAN mode v10.0 in bot
> Note: History will reset when using /danmode command!!

<br>

# ▋Common Issue: Empty API Responses
### Problem Description
The problem often arises when the API doesn't return the expected data (empty string), affecting the functionality of the chat bot. I used error handler to handle this empty result and send `[Empty Result]` to the user instead of raising error from Telegram! <br>
This issue is caused by problems with the external API (Maybe IP limitation or bot chanllenges).

### Solutions
For now, simple solution is to resend your prompt and ask your question again.

### Contributions
I welcome contributions. If you've found a reliable solution to this issue or have other useful suggestions, please consider contributing to this project.

<br>

# ▋Features
This bot responds to every message with ChatGPT AI, excluding commands.
+ Inline mode for obtaining predefined roles. [**How to use**](https://github.com/Kourva/AwesomeChatGPTBot/issues/3)
+ The ability to remember chat history.

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
