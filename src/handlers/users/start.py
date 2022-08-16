from aiogram.dispatcher import filters
import aiogram.types

from services import db_api
import services.db_api.session
import responses.start
from loader import dp


@dp.message_handler(filters.builtin.CommandStart())
async def start(message: aiogram.types.Message):
    full_name = message.from_user.full_name
    await responses.start.StartResponse(message, full_name)
    with services.db_api.session.Session() as session, session.begin():
        db_api.add_user_to_db(session, message.from_user.id, full_name)
