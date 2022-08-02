from aiogram.dispatcher import filters
from aiogram import types

from loader import dp
import responses.help


@dp.message_handler(filters.CommandHelp())
async def get_help(message: types.Message):
    await responses.help.HelpResponse(message)
