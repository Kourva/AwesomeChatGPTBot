<div align="center">
    <img align='center' src="https://github.com/Kourva/AwesomeChatGPTBot/assets/118578799/ef1cfefd-1e58-45d3-8a3a-fa9988a8322e" width=200 height=200 />
    <p align='center'><b>Free ChatGPT Telegram Bot with Multiple Providers support!</b></p>
    <p align='center'>No APi-Key | Pre-Defiened Roles | Inline mode | Dan Mode</p>
</div>
<br><br>

# ＃ Status
New version is here with new codebase and features: <br>
+ python 3.15 and cleaner source + ruff <br>
+ async version <br>
+ multiple chat sessions <br>
+ new sqlite database instead of raw json database <br>
+ new streaming feature for the response <br>
+ history now supports multiple sessions <br>
+ new support for the CloudFlare proxy for restricted countries: [worker](https://github.com/Kourva/cloudflare-workers/#-tba)<br>
+ new working providers: [issue](https://github.com/Kourva/AwesomeChatGPTBot/issues/101) <br>
+ new TTS provider with defaults to google [issue](https://github.com/Kourva/AwesomeChatGPTBot/issues/98) <br>
+ analyzing a larger text file as file/image input: [issue](https://github.com/Kourva/AwesomeChatGPTBot/issues/94) <br>
+ auto updater for systemd, OpenRC or runit: [issue](https://github.com/Kourva/AwesomeChatGPTBot/issues/66) <br>
+ i18n for multiple language support: [issue](https://github.com/Kourva/AwesomeChatGPTBot/issues/30)

<br>

# ＃ Providers
Bot includes multiple free providers (Thanks to [gpt4free](https://github.com/xtekky/gpt4free)). it tries all providers one by one to respond and breaks the loop in first valid response. So you don't have to select provider and if non of the providers worked, bot will tell you to generate your prompt again.<br>
You can send `/settings` command to bot to change these providers (Enable/Disable)

<br>

# ▋Bot is Down? Not working?
Since bot is supporting multiple providers now, you can use `/ping` to check which one is working.

### Contributions
I welcome contributions. If you've found a reliable solution to this issue or have other useful suggestions, please consider contributing to this project.

<br>

# ▋Features
This bot responds to every message with ChatGPT AI and other models like llama, excluding commands.
+ Inline mode for obtaining predefined roles. [**How to use**](https://github.com/Kourva/AwesomeChatGPTBot/issues/3#issuecomment-1791705893)
+ The ability to remember chat history.
+ Multiple providers.
+ Voice response.
+ Provider settings (use /settings)

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
> + `/tts`
> + `/settings`

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
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=Kourva/AwesomeChatGPTBot&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=Kourva/AwesomeChatGPTBot&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=Kourva/AwesomeChatGPTBot&type=Date" />
</picture>
