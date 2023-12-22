<p align="center">
    <img align='left' src="https://github.com/Kourva/AwesomeChatGPTBot/assets/118578799/ef1cfefd-1e58-45d3-8a3a-fa9988a8322e" width=200 height=200/>
    <h2>Free Chat GPT Telegram Bot </h2>
  <p><b>Free ChatGPT-3.5 Telegram Bot with Multiple Providers support!</b></p>
  <p><b>No APi-Key | Pre-Defiened Roles | Inline mode | Dan Mode v10</b></p>
</p>
<br><br>

# ▋Change Log
[**Last Status: Dec 22, 2023**]: Bot updated! see changes below.<br>
See more logs [here](#full-change-log)


<br>

# ▋Upcoming Features
1. **Smart reply**: Reply to user's message to process them with GPT.<br>
2. **Code Generator**: Use code generator to generate functions in many languages.<br>
3. **Image generator**: Use AI to generate images from prompt.
4. ~~**Multiple models**: Use multiple providers~~ **(DONE)**<br>
5. **Multiple language**: Bot supports multiple languages for better communication. (Idea by [chelaxian](https://github.com/chelaxian) | [Issue](https://github.com/Kourva/AwesomeChatGPTBot/issues/30))

<br>

# Multiple Providers
From now bot includes multiple providers (Thanks for [gpt4free](https://github.com/xtekky/gpt4free)).<br>
For responding, bot tries all providers one by one to respond and breaks the loop in first valid response. So you don't have to select provider.
If non of providers worked, bot will tell you to generate your prompt again.<br>
**List of available providers**:
+ **FakeOpen Ai** (uses model ChatGPT 3.5 Turbo)
+ **Fstha Chat** (uses model ChatGPT 3.5 Turbo)
+ **DeepInfra AI** (uses model Llama 2 70b Chat hf)
+ **Online GPT** (uses model ChatGPT 3.5 Turbo)

<br>

# ▋Bot is Down? Not working?
Since bot is supporting multiple providers now, you can use `/ping` to check which one is working.

### Contributions
I welcome contributions. If you've found a reliable solution to this issue or have other useful suggestions, please consider contributing to this project.

<br>

# ▋Features
This bot responds to every message with ChatGPT AI and other models like llama, excluding commands.
+ Inline mode for obtaining predefined roles. [**How to use**](https://github.com/Kourva/AwesomeChatGPTBot/issues/3#issuecomment-1791705893)
+ The ability to remember chat history (long-term memory).
+ Multiple providers.

<br>

# ▋Clone Repository
To get started, first you need to **clone** this repository from github into your machine:
```bash
git clone https://github.com/Kourva/AwesomeChatGPTBot
```
> if you dont have git or python you can install it from your package manager!

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
This will install **pyTelegamBotAPI** and **Requests** for you, You can also install them manually if you got any error:
```bash
pip install pyTelegamBotAPI Requests
```

<br>

# ▋Configure your token
Now you have to create bot from [BotFather](https://t.me/BotFather) **(If you don't have)** and get your **Token** to start working with your bot.<br>
After getting **Token** from **BotFather** replace the Token in `token.txt`
```plaintext
0000000000:AAE7fbH29UPOKzlHlp0YDr9o06o_NdD4DBk
```
You can use editors like 'nano' or 'vim' in Termux or using echo command to write token to file:
```bash
echo "0000000000:AAE7fbH29UPOKzlHlp0YDr9o06o_NdD4DBk" > token.txt
```
> This is just an example Token. 

<br>

# ▋Configure the bot commands (Optional)
you can set your bot's commands manually or using 'init.py' script
```bash
python init.py
```
> This will set up these commands in bot's menu
> + `/start`
> + `/help`
> + `/ping`
> + `/chat`
> + `/features`
> + `/history`
> + `/reset`
> + `/danmode`

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
It depends on you to use `strict_chain` or `dynamic_chain`. Config it by yourself.
<br>

# ▋TOR new IP address
If you got any denied requests that blocked your Ip address, you can renew your IP
```bash
sudo killall -HUP tor
```
And if you want to check your TOR status, use this command:
```bash
proxychains curl https://check.torproject.org/api/ip
```

<br>

# ▋Bot Inline Mode
Don't forget to enable **Inline Mode** in your bot.<br>
See documentation here: https://core.telegram.org/bots/api#inline-mode

<br>

# ▋Thanks a bunch for starring the project! :star:
If you have any suggestions or feedback, feel free to share. I appreciate your interest and contribution to the project!

<picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=kourva/AwesomeChatGPTBot&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=kourva/AwesomeChatGPTBot&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=kourva/AwesomeChatGPTBot&type=Date" />
</picture>

<br>

# ▋Full Change Log
**[Dec 22, 2023]** Added Multiple Providers.<br>
**[Dec 22, 2023]** Added `/ping` command to ping providers.<br>
**[Dec 22, 2023]** Removed `/setting` command and setting files for users.<br>
**[Dec 22, 2023]** Added more exception handlers for both Connection and Telegram API.<br>

<br>

**[Dec 01, 2023] Smarter Re-generate:** Uses smarter way to re-generate replied question.<br>
**[Dec 01, 2023] Settings command:** Added setting command to change bot response setting.<br>
**[Dec 01, 2023] Added titles.py:** To make main code more clear.<br>
**[Dec 01, 2023] Error handling:** Added more handlers and depp link handlers.<br> 
**[Nov 13, 2023] PEP8 fixes:** Fixed some PEP8 issues.<br>
**[Nov 13, 2023] Extra commands:** Added `help`, `features` and `chat` commands.<br>
**[Nov 13, 2023] MarkdownV2:** Added converter to convert regular markdown to Markdown V2.<br>
**[Nov 13, 2023] History management**: Added utilities to check history and fix it when it got broken.<br>
**[Nov 13, 2023] Re-Generate**: Users can re-generate their prompts, new answer will be raplaced with old one<br>
**[Nov 13, 2023] Improved chat handler**: Users now requied to use /chat in groups to chat with bot.<bt>
```
/chat hi
```
> This will avoid mess in replies and even reactions to bot's responses.

**[Nov 01, 2023] History command:** Added history section added (use /history to get history file)<br>
**[Nov 01, 2023] History reset:** Added /reset command to reset the chat history.<br>
**[Nov 01, 2023] Dan mode v10:** Added /danmode** command to enable/disable DAN mode v10.0 in bot.<br>
> Note: History will reset when using /danmode command!!
