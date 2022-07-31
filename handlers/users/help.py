from aiogram.dispatcher import filters
from aiogram import types

from loader import dp


@dp.message_handler(filters.CommandHelp())
async def get_help(message: types.Message):
    await message.answer(
        '/start - Start bot\n'
        '/help - Get help\n'
        '/add_quote - Add quote\n'
        '$$ - Quickly Add quote\n'
        '(The author is marked with @, tags - #)'
        )
