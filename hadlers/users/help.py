from aiogram import types
from aiogram.dispatcher.filters import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def get_help(message: types.Message):
    await message.answer(
        '/start - Запутсить бота'
        '/help - Получить справку'
        '/add_quote - Добавить цитату'
        '/quick_add_quote - Доавить цитату быстрее\n'
        '(Автор помечается знаком @, теги - #)'
        )