<div align="center">
    <img align='center' src="https://github.com/Kourva/AwesomeChatGPTBot/assets/118578799/ef1cfefd-1e58-45d3-8a3a-fa9988a8322e" width=200 height=200 />
    <p align='center'><b>A free, multi-provider AI Telegram bot. no API key needed</b></p>
    <p align='center'>No API-Key | Pre-Defined Roles | Chat Sessions | Inline Mode | DAN Mode</p>
    <p align='center'>Chat ⋆ Images ⋆ Voice ⋆ Web search ⋆ Multiple languages</p>
</div>

<br><br>

# ＃ What's new in v2
A full rewrite. same idea, cleaner and async. The old code is archived on the `old-source` branch.

+ Python 3.15, async source, ruff
+ multiple chat sessions, each with its own history and export
+ streaming responses
+ sqlite storage (replaces the old raw JSON database)
+ multiple free providers. `/ping` to check, `/settings` to toggle
+ image generation. `/image`
+ text-to-speech. `/tts` (StreamElements by default, Voicepods optional)
+ vision & text-file analysis (needs an OpenRouter or DeepInfra key)
+ i18n: en, fa, ru, tr, so. `/language`
+ CloudFlare worker proxy for restricted countries
+ auto-updater for systemd, OpenRC and runit

### Issues & thanks
Feature requests and bugs that shaped this release:
[#101](https://github.com/Kourva/AwesomeChatGPTBot/issues/101) providers,
[#98](https://github.com/Kourva/AwesomeChatGPTBot/issues/98) TTS,
[#94](https://github.com/Kourva/AwesomeChatGPTBot/issues/94) file/image input,
[#66](https://github.com/Kourva/AwesomeChatGPTBot/issues/66) auto-updater,
[#30](https://github.com/Kourva/AwesomeChatGPTBot/issues/30) i18n,
[#3](https://github.com/Kourva/AwesomeChatGPTBot/issues/3) inline roles

Thanks to everyone who opened issues, sent PRs and tested the bot:
[@chelaxian](https://github.com/chelaxian), [@Kritik-helpingai](https://github.com/Kritik-helpingai), [@tommy04062019](https://github.com/tommy04062019), [@Vichima](https://github.com/Vichima)

<br><br>

# ＃ Quick help
Just send a message in private chat. no command needed. In groups use `/chat`.

| Command | What it does |
|---|---|
| `/start` | Welcome screen and shortcut menu |
| `/chat <text>` | Talk to the AI (required in groups) |
| `/image <prompt>` | Generate an image |
| `/tts <text>` | Get a voice reply |
| `/session` | List, create (`/session new`) or rename (`/session title <name>`) chats |
| `/history` | Pick a chat and download its history |
| `/reset` | Clear the current chat history |
| `/settings` | Enable or disable providers |
| `/ping` | Check which providers are online |
| `/language en\|fa\|ru\|tr\|so` | Change the bot language |
| `/danmode` | Toggle DAN mode (clears history) |
| `/help` | Show the command list |

**Inline mode**
- `@yourbot roles`. pick a predefined role.
- `@yourbot web <query>`. web search inline (beta, depends on providers).

**Uploads**
Send a photo or a text file (`txt, md, csv, json`, …) with a caption and the bot analyzes it. Images need a vision-capable provider. set `OPENROUTER_API_KEY` or `DEEPINFRA_API_KEY` in `.env`, otherwise the bot tells you no provider can read images yet.

**Sessions**
Each chat is a separate session with its own history. `/session` opens a list. tap one to make it active, create a new one, or rename it. `/history` exports the selected chat as a file.

<br><br>

# ＃ Providers
The bot ships with several free providers (Pollinations, Phind, DeepInfra, OpenRouter) plus TTS via StreamElements or Voicepods. It tries them one by one and returns the first valid answer, so you don't have to pick one. and if none work, it asks you to try again. Open `/settings` to enable or disable providers, and `/ping` to see which are currently up.

DeepInfra and OpenRouter also power image understanding when their API key is set.

<br><br>

# ＃ Proxy for restricted countries
Two options. Use whichever fits your setup.

### CloudFlare worker (faster but requires little bit of working)
Deploy the worker from [Kourva/cloudflare-workers](https://github.com/Kourva/cloudflare-workers), then point the bot at it in `.env`:

```env
PROXY_URL=https://your-worker.workers.dev
PROXY_SECRET=your-shared-secret
```

PROXY_SECRET must match the secret configured in the worker. When PROXY_URL is set, the bot sends its API traffic through the worker.

### Tor via proxychains
+ Install proxychains-ng, edit /etc/proxychains.conf (strict_chain or dynamic_chain. your call), then:
```bash
proxychains python src/main.py
# quiet mode
proxychains -q python src/main.py
```

+ Renew your Tor IP if requests get blocked:
```bash
sudo killall -HUP tor
```

+ Check that Tor is working:
```bash
proxychains curl https://check.torproject.org/api/ip
```

<br><br>

# ＃ Install
Requires Python 3.15+, git, and pip.
  
```bash
git clone https://github.com/Kourva/AwesomeChatGPTBot
cd AwesomeChatGPTBot

python3 -m venv .venv

# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
```

Create the config and fill it in:

```bash
cp .env.example .env
```

At minimum set BOT_TOKEN (from @BotFather) and ADMIN_ID. Everything else is optional. see .env.example for the full list (proxy, database path, default language, history limit, TTS voice/provider, DeepInfra/OpenRouter keys and vision models).

Run it:

```bash
python src/main.py
```

<br><br>

# ＃Run as a service & auto-update
`scripts/install.sh` installs the bot as a service and sets up a daily auto-update. It supports systemd, OpenRC and runit, and picks whichever is present.
```bash
sudo ./scripts/install.sh
```

What it does:
- creates .venv (if missing) and installs requirements.txt
- writes service config to /etc/default/acgptb-bot
- installs and starts the service (default name acgptb-bot)
- schedules the updater. a systemd timer at 04:00, or a cron entry in /etc/cron.d/acgptb-bot-update for OpenRC/runit

Override defaults with environment variables:
    ```bash
    sudo SERVICE_NAME=mybot BRANCH=main PYTHON=python3 ./scripts/install.sh
    ```
Updates are handled by scripts/update.sh. It keeps .env, .venv, the database and caches, pulls the latest code (git fetch + --ff-only merge, or a fresh clone + rsync if there's no .git), reinstalls requirements and restarts the service.

The updater runs automatically every day, or manually:

```bash
sudo ./scripts/update.sh
```

Manage the service:
```bash
# systemd
systemctl status acgptb-bot
systemctl restart acgptb-bot

# OpenRC
rc-service acgptb-bot status

# runit
sv status acgptb-bot
```

<br><br>

# ＃ Inline mode (beta)
Enable Inline Mode for your bot in @BotFather (/setinline).

- @yourbot roles: pick a predefined role.
- @yourbot web <query>: web search inline. Beta: results depend on the upstream provider, so it may fail when that provider is down. Try again later.

<br><br>

# ＃ Thanks a bunch for starring the project! :star:
If you have any suggestions or feedback, feel free to share. I appreciate your interest and contribution to the project!

<picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=Kourva/AwesomeChatGPTBot&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=Kourva/AwesomeChatGPTBot&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=Kourva/AwesomeChatGPTBot&type=Date" />
</picture>
