import aiogram.types

from keyboards.inline import edit_quote_keyboard
from utils import db_api
import utils.db_api.session
from loader import dp
import responses.quote


@dp.callback_query_handler(keyboards.inline.callback_data.quote_cb.filter(action='select'))
async def get_quote(query: aiogram.types.CallbackQuery, callback_data: dict):
    with db_api.session.Session() as session, session.begin():
        quote = db_api.get_quote_by_order_in_user(session, int(callback_data['id']))
    await responses.quote.QuoteMenuResponse(query, quote)
