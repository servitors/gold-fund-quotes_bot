from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.message_handler(state='*')
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
