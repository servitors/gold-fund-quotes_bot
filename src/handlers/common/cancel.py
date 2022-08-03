from aiogram.dispatcher import filters
from aiogram import dispatcher
import aiogram.types

from src.loader import dp


@dp.message_handler(filters.Command('cancel'), state='*')
async def cancel(message: aiogram.types.Message, state: dispatcher.FSMContext):
    await message.answer('Canceled')
    await state.finish()
