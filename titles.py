# Titles for chatGPT bot
# So i store texts and titles here to avoid mess in main code.

# We have 4 type of welcome messages
# First 2 is normal and second 2 is for deep-linking
# User is new (/start):
welcome_1 = (
    "Hi {}\n\n"
    "Welcome to ChatGPT bot!\n"
    "Press /help if you need any help..."
)
# User already have account (/start):
welcome_2 = (
    "Welcome back {}\n"
    "Let's begin chat!"
)
# User is new (/start=create):
welcome_3 = (
    "Hi {}\n"
    "Your account has been created! Enjoy."
)
# User already have account (/start?create):
welcome_4 = (
    "Hi {}\n"
    "You already have account."
)

# No account prompt for users with no accounts:
no_account_warn = (
    "Dear {}\n\n"
    "You need to start the bot before using it! "
    "We need to create an account for you first:\n\n"
    "t.me/{}?start=create"
)

# History cleared prompt:
history_cleared = (
    "Dear {}\n\n"
    "Your history cleared successfully."
)

# Dan mode prompts for /danmode command
# Dan mode enabled:
dan_mode_enabled = (
    "DAN mode _version 10.0!_\n"
    "Status: *Enabled*"
)
# Dan mode disabled:
dan_mode_disabled = (
    "DAN mode _version 10.0!_\n"
    "Status: *Disabled*\n\n"
    "Note: History file also reset!"
)

# Help prompt for (/help) command:
help_message = (
    "*List of global commands*:\n"
    "1. /start: Start bot\n"
    "2. /help: Show this message\n"
    "3. /ping: Ping the Providers\n\n"
    "*List of chat related commands*:\n"
    "1. /reset: Reset chat history\n"
    "2. /history: Get chat history\n"
    "3. /chat: Chat in groups\n"
    "4. /danmode: Use DAN mode in GPT\n\n"
    "*Other commands*:\n"
    "1. /features: See feature changes\n\n"
    "*Inline usage*:\n"
    "`\n@{} roles`\n"
    "this will show all available roles.\n\n"
    "*Chat command usage*:\n"
    "`\n/chat hello world!`"
)

# Features prompt for (/features) command
features = (
    "*Main features*:\n"
    "1. Includes long-term memory\n"
    "2. Includes roles and DAN mode\n"
    "3. Supports both group and private chat\n"
    "4. Includes re-generate option\n\n"
    "*Other features*:\n"
    "1. MarkdownV2 escaper\n"
    "2. History checker and fixer\n\n"
    "*Upcoming Features*:\n"
    "1. Smart reply option\n"
    "2. Code generator\n"
    "3. Image generator\n"
    "4. Voice response\n"
    "5. Multi language\n\n"
    "Please submit your Issue or Request in here:\n"
    "https://github.com/Kourva/AwesomeChatGPTBot/issues\n\n"
    "*Recent changes*:\n"
    "# Added multiple providers.\n"
    "# Changes on commands.\n"
    "# Changes on user configs file."
)

# Usage help for (/chat) command:
chat_help = (
    "Hi {}\n"
    "Please Ask your question after /chat\n\n"
    "*Example*: /chat hi"
)

# Response prompt:
response_prompt = (
    "Generating response... Please wait."
)


# GPT response error:
response_error = (
    "Error!\n"
    "ChatGPT is not responding at this time!"
)
