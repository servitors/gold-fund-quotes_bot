import aiogram.types

from src.keyboards.inline import edit_quote_keyboard
from src.utils import db_api
from src.loader import dp


@dp.callback_query_handler(keyboards.inline.callback_data.quote_cb.filter(action='select'))
async def get_quote(query: aiogram.types.CallbackQuery, callback_data: dict):
    quote = db_api.get_quote_by_order_in_user(int(callback_data['id']))
    current_page = int(callback_data['id']) // 10
    keyboard = edit_quote_keyboard.EditQuoteKeyboard(quote.order_in_user, current_page)
    await query.message.edit_text(text=messages.quote_constructor(quote.content, quote.author))
    await query.message.edit_reply_markup(reply_markup=keyboard)
