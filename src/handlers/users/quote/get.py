from aiogram.dispatcher import filters
import aiogram.types

from utils import db_api
import utils.db_api.session
from loader import dp
import utils.quote


@dp.inline_handler()
async def get_quote_in_inline_mode(query: aiogram.types.InlineQuery):
    query_offset = int(query.offset) if query.offset else 1
    tags = query.query.split()
    with db_api.session.Session() as session, session.begin():
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
    user_id = message.from_user.id
    with db_api.session.Session() as session, session.begin():
        quotes = db_api.get_user_quotes(session, user_id, page=0, page_size=10)
    menu = quote_menu.QuoteMenuKeyboard(quotes, page=0, action='select')
    await message.answer(text='Quote Menu', reply_markup=menu)


@dp.callback_query_handler(quote_menu.QuoteMenuKeyboard.navigation_buttons_cb.filter(action='navigate'))
async def navigate_quote_menu(query: aiogram.types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    page = callback_data['page']
    with db_api.session.Session() as session, session.begin():
        quotes = db_api.get_user_quotes(session, user_id, page=page, page_size=10)
    menu = quote_menu.QuoteMenuKeyboard(quotes, page=page, action='select')
    await query.message.edit_text(text='Quote Menu')
    await query.message.edit_reply_markup(reply_markup=menu)
    await query.answer()
