import aiogram.types

from keyboards.inline import callback_factories
from utils import db_api
import utils.db_api.session
from loader import dp
import responses.quote


@dp.callback_query_handler(callback_factories.QuoteMenuCallbackFactory().filter(action='select'))
async def get_quote(query: aiogram.types.CallbackQuery, callback_data: dict):
    with db_api.session.Session() as session, session.begin():
        quote = db_api.get_user_by_id(session, int(callback_data['id']))
    await responses.quote.QuoteMenuResponse(query, quote)
