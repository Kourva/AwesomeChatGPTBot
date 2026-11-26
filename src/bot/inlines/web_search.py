import aiohttp
from telebot.async_telebot import AsyncTeleBot
from telebot.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    LinkPreviewOptions,
)

ENDPOINT = "https://api.contextfetch.dev/v1/search"


async def search(query: str) -> dict | None:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            ENDPOINT,
            json={
                "query": query,
                "numResults": 10,
                "contents": {
                    "text": True,
                    "highlights": True,
                    "pruned_context": True,
                },
            },
        ) as response:
            if response.status != 200:
                return None
            return await response.json()


def web_search_inline(bot: AsyncTeleBot) -> None:
    @bot.inline_handler(func=lambda query: query.query.lower().startswith("web "))
    async def _(inline_query: InlineQuery) -> None:
        query = inline_query.query[4:].strip()
        if not query:
            await bot.answer_inline_query(
                inline_query.id,
                [
                    InlineQueryResultArticle(
                        id="usage",
                        title="Use: @bot web your question",
                        description="Add a question after the web prefix",
                        input_message_content=InputTextMessageContent(
                            message_text="Use: @bot web your question"
                        ),
                    )
                ],
                cache_time=0,
            )
            return

        try:
            response = await search(query)
        except aiohttp.ClientError:
            response = None

        results = []
        for index, item in enumerate((response or {}).get("results", [])):
            url = item.get("url", "")
            results.append(
                InlineQueryResultArticle(
                    id=str(index),
                    title=item.get("title") or "Untitled",
                    description=url,
                    input_message_content=InputTextMessageContent(
                        message_text=f"{item.get('title')}\n{url}",
                        link_preview_options=LinkPreviewOptions(
                            prefer_small_media=True,
                            url=url,
                        ),
                    ),
                )
            )

        if not results:
            results.append(
                InlineQueryResultArticle(
                    id="empty",
                    title="No results",
                    description="Nothing found, try another query",
                    input_message_content=InputTextMessageContent(
                        message_text=f"No results for: {query}"
                    ),
                )
            )

        await bot.answer_inline_query(inline_query.id, results, cache_time=30)
