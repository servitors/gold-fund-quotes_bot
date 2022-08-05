from aiogram.dispatcher import filters
import aiogram.types

from utils import db_api
import responses.start
from loader import dp


@dp.message_handler(filters.builtin.CommandStart())
async def start(message: aiogram.types.Message):
    full_name = message.from_user.full_name
    await responses.start.StartResponse(message, full_name)
    db_api.add_user_in_db(message.from_user.id, full_name)
