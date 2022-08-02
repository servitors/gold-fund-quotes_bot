from aiogram.dispatcher import filters
import aiogram.types

from keyboards.inline import quote_menu
from utils import db_api, messages, pagination
from loader import dp


@dp.inline_handler()
async def get_quote_in_inline_mode(query: aiogram.types.InlineQuery):
    query_offset = int(query.offset) if query.offset else 1
    tags = query.query.split()
    quotes = db_api.get_quotes_by_tags(query.from_user.id, tags)
    articles = [aiogram.types.InlineQueryResultArticle(
        id=str(n),
        title=item.author,
        description=item.content,
        input_message_content=aiogram.types.InputTextMessageContent(
            message_text=messages.quote_constructor(item.content, item.author)
        )
    ) for n, item in enumerate(quotes)]

    if len(articles) < 50:
        await query.answer(articles, is_personal=True, next_offset="")

    await query.answer(articles, cache_time=60, is_personal=True, next_offset=str(query_offset + 50))


@dp.message_handler(filters.Command('quote_menu'))
async def quote_menu(message: aiogram.types.Message):
    user_id = message.from_user.id
    quotes = db_api.get_user_quotes_in_range(user_id, range(0, 10))
    menu = quote_menu.QuoteMenuKeyboard(quotes, page=0, action='select')
    await message.answer(text='Quote Menu', reply_markup=menu)


@dp.callback_query_handler(quote_menu.QuoteMenuKeyboard.navigation_buttons_cb.filter(action='navigate'))
async def navigate_quote_menu(query: aiogram.types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    elements_on_page = 10
    quantity = db_api.count_quote(user_id)
    paginator = pagination.Pagination(quantity, int(callback_data['page']), elements_on_page)
    quotes = db_api.get_user_quotes_in_range(user_id, paginator.range_elements)
    menu = quote_menu.QuoteMenuKeyboard(quotes, paginator.page, action='select')
    await query.message.edit_text(text='Quote Menu')
    await query.message.edit_reply_markup(reply_markup=menu)
    await query.answer()
