import aiogram.types
from aiogram import dispatcher
from aiogram.dispatcher import filters

from loader import dp


@dp.message_handler(filters.Command('cancel'), state='*')
async def cancel(message: aiogram.types.Message, state: dispatcher.FSMContext):
    await message.answer('Canceled')
    await state.finish()
