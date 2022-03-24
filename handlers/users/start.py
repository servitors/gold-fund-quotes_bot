from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils.db_api import add_user_in_db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    await message.answer(f"Hello, {name}")
    add_user_in_db(message.from_user.id, name)
