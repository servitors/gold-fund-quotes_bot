from aiogram.dispatcher import filters
from aiogram import types

from utils import db_api
from loader import dp


@dp.message_handler(filters.builtin.CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    await message.answer(f"Hello, {name}")
    db_api.add_user_in_db(message.from_user.id, name)
