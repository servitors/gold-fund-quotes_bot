from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.inline.pagination import Paginator
from keyboards.inline.quote_menu import QuoteMenuKeyboard
from loader import dp
from utils.db_api import get_quotes_by_tags, count_quote, get_user_quotes_in_range
from utils.misc.messages import message_constructor


@dp.inline_handler()
async def get_quote_in_inline_mode(query: types.InlineQuery):
    query_offset = int(query.offset) if query.offset else 1
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

    if len(articles) < 50:
        await query.answer(articles, is_personal=True, next_offset="")

    await query.answer(articles, cache_time=60, is_personal=True, next_offset=str(query_offset + 50))


@dp.message_handler(Command('quote_menu'))
async def quote_menu(message: types.Message):
    user_id = message.from_user.id
    quotes = get_user_quotes_in_range(user_id, range(0, 10))
    menu = QuoteMenuKeyboard(quotes, page=0, action='select')
    await message.answer(text='Quote Menu', reply_markup=menu)


@dp.callback_query_handler(QuoteMenuKeyboard.navigation_buttons_cb.filter(action='navigate'))
async def navigate_quote_menu(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    elements_on_page = 10
    quantity = count_quote(user_id)
    paginator = Paginator(quantity, int(callback_data['page']), elements_on_page)
    quotes = get_user_quotes_in_range(user_id, paginator.range_elements)
    menu = QuoteMenuKeyboard(quotes, paginator.page, action='select')
    await query.message.edit_text(text='Quote Menu')
    await query.message.edit_reply_markup(reply_markup=menu)
    await query.answer()
