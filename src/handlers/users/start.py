import aiogram.types
from aiogram.dispatcher import filters

import responses.start
from loader import dp
from services import db_api


@dp.message_handler(filters.builtin.CommandStart())
async def start(message: aiogram.types.Message):
    full_name = message.from_user.full_name
    await responses.start.StartResponse(message, full_name)
    with db_api.create_session() as session:
        db_api.add_user_to_db(session, message.from_user.id, full_name)
