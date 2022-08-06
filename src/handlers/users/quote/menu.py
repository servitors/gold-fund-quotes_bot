import aiogram.types

from keyboards.inline import edit_quote_keyboard
from utils import db_api
import utils.db_api.session
from loader import dp


@dp.callback_query_handler(keyboards.inline.callback_data.quote_cb.filter(action='select'))
async def get_quote(query: aiogram.types.CallbackQuery, callback_data: dict):
    with db_api.session.Session() as session, session.begin():
        quote = db_api.get_quote_by_order_in_user(session, int(callback_data['id']))

    current_page = int(callback_data['id']) // 10
    keyboard = edit_quote_keyboard.EditQuoteKeyboard(quote.order_in_user, current_page)
    await query.message.edit_text(text=messages.quote_constructor(quote.content, quote.author))
    await query.message.edit_reply_markup(reply_markup=keyboard)
