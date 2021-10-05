from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command('cancel'), state='*')
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
