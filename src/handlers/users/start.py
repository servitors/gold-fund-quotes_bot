from aiogram.dispatcher import filters
from aiogram import types

from src.responses import start
from src.utils import db_api
from src.loader import dp


@dp.message_handler(filters.builtin.CommandStart())
async def start(message: types.Message):
    full_name = message.from_user.full_name
    await start.StartResponse(message, full_name)
    db_api.add_user_in_db(message.from_user.id, full_name)
