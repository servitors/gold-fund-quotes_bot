import aiogram.types

from keyboards.inline import callback_factories
from services import db_api
import services.db_api.session
from loader import dp
import responses.quote


@dp.callback_query_handler(callback_factories.QuoteMenuCallbackFactory().filter(action='select'))
async def get_quote(query: aiogram.types.CallbackQuery, callback_data: dict):
    with services.db_api.session.Session() as session, session.begin():
        quote = db_api.get_user_quote(session, int(callback_data['id']), user_id=query.from_user.id)
    await responses.quote.QuoteMenuResponse(query, quote)
