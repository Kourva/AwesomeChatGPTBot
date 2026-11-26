from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from bot.data.prompts import ROLE_PROMPTS


def roles_inline(bot: AsyncTeleBot) -> None:
    @bot.inline_handler(func=lambda query: query.query.lower().startswith("roles"))
    async def _(inline_query: InlineQuery) -> None:
        search = inline_query.query[5:].strip().lower()
        results = []

        for index, (title, prompt) in enumerate(ROLE_PROMPTS.items()):
            if search and search not in title.lower():
                continue
            results.append(
                InlineQueryResultArticle(
                    id=str(index),
                    title=title,
                    description=prompt[:100],
                    input_message_content=InputTextMessageContent(message_text=prompt),
                )
            )

        await bot.answer_inline_query(inline_query.id, results[:50], cache_time=300)
