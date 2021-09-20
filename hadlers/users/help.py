from aiogram import types
from aiogram.dispatcher.filters import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def get_help(message: types.Message):
    await message.answer(
        '/start - Запутсить бота\n'
        '/help - Получить справку\n'
        '/add_quote - Добавить цитату\n'
        '/quick_add_quote - Доавить цитату быстрее\n'
        '(Автор помечается знаком @, теги - #)'
        )