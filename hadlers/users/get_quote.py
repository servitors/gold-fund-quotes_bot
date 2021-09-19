from aiogram import types

from loader import dp
from utils.db_api import get_quotes_by_tags
from utils.misc.message_worker import message_constructor


@dp.inline_handler()
async def get_quote_in_inline_mode(query: types.InlineQuery):
    tags = query.query.split()
    quotes = get_quotes_by_tags(query.from_user.id, tags)
    articles = [types.InlineQueryResultArticle(
        id=str(n),
        title=item.author,
        description=item.content,
        input_message_content=types.InputTextMessageContent(
            message_text=message_constructor(item.content, item.author)
            )
        ) for n, item in enumerate(quotes)]
    await query.answer(articles, cache_time=60, is_personal=True)
