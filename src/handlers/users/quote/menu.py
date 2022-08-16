import aiogram.types

import responses.quote
from keyboards.inline import callback_factories
from loader import dp
from services import db_api


@dp.callback_query_handler(callback_factories.QuoteMenuCallbackFactory().filter(action='select'))
async def get_quote(query: aiogram.types.CallbackQuery, callback_data: dict):
    with db_api.create_session() as session:
        quote = db_api.get_user_quote(session, int(callback_data['id']), user_id=query.from_user.id)
    await responses.quote.QuoteMenuResponse(query, quote)
