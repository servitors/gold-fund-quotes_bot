from aiogram.dispatcher import filters
from aiogram import types

from src.loader import dp
import src.responses.help


@dp.message_handler(filters.CommandHelp())
async def help_message(message: types.Message):
    await src.responses.help.HelpResponse(message)
