import aiogram.types
from aiogram.dispatcher import filters

import responses.help
from loader import dp


@dp.message_handler(filters.CommandHelp())
async def help_message(message: aiogram.types.Message):
    await responses.help.HelpResponse(message)
