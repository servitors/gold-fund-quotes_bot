from aiogram import types

from keyboards.inline.callback_data import quote_cb
from keyboards.inline.edit_quote_keyboard import EditQuoteKeyboard
from loader import dp
from utils.db_api import get_quote_by_order_in_user
from utils.misc.message_worker import message_constructor


@dp.callback_query_handler(quote_cb.filter(action='select'))
async def get_quote(query: types.CallbackQuery, callback_data: dict):
    quote = get_quote_by_order_in_user(int(callback_data['id']))
    current_page = int(callback_data['id']) // 10
    keyboard = EditQuoteKeyboard(quote.order_in_user, current_page)
    await query.message.edit_text(text=message_constructor(quote.content, quote.author))
    await query.message.edit_reply_markup(reply_markup=keyboard)
