import aiogram.types
from aiogram.dispatcher import filters

import responses.quote
import utils.quote
from keyboards.inline import callback_factories
from loader import dp
from services import db_api


@dp.inline_handler()
async def get_quote_in_inline_mode(query: aiogram.types.InlineQuery):
    query_offset = int(query.offset) if query.offset else 1
    tags = query.query.split()
    with db_api.create_session() as session:
        quotes = db_api.get_quotes_by_tags(session, query.from_user.id, tags)
    articles = [aiogram.types.InlineQueryResultArticle(
        id=str(n),
        title=item.author,
        description=item.content,
        input_message_content=aiogram.types.InputTextMessageContent(
            message_text=utils.quote.quote_constructor(item.content, item.author)
        )
    ) for n, item in enumerate(quotes)]

    if len(articles) < 50:
        await query.answer(articles, is_personal=True, next_offset="")

    await query.answer(articles, cache_time=60, is_personal=True, next_offset=str(query_offset + 50))


@dp.message_handler(filters.Command('quote_menu'))
async def quote_menu(message: aiogram.types.Message):
    with db_api.create_session() as session:
        quotes = db_api.get_user_quotes(session, message.from_user.id, page=0, page_size=10)
    await responses.quote.QuotesResponse(message, quotes)


@dp.callback_query_handler(callback_factories.QuotesCallbackFactory().filter())
async def quote_menu(query: aiogram.types.CallbackQuery, callback_data: dict):
    page = int(callback_data['page'])
    with db_api.create_session() as session:
        quotes = db_api.get_user_quotes(session, query.from_user.id, page=page, page_size=10)
    await responses.quote.QuotesResponse(query, quotes, page)
