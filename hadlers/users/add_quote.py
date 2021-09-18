from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from states.order_quote import *
from utils.db_api import add_quote_in_db, Tag
from utils.misc.message_worker import *


@dp.message_handler(Command('add_quote'))
async def add_quote_command(message: types.Message):
    await OrderQuote.waiting_for_quote_content.set()
    await message.answer('Введите цитату')


@dp.message_handler(state=OrderQuote.waiting_for_quote_content)
async def content_quote(message: types.Message, state: FSMContext):
    await state.update_data(content=message.text)
    await OrderQuote.waiting_for_quote_author.set()
    await message.answer('Укажите автора')


@dp.message_handler(state=OrderQuote.waiting_for_quote_author)
async def author_quote(message: types.Message, state: FSMContext):
    await state.update_data(author=message.text)
    await OrderQuote.waiting_for_quote_tags.set()
    await message.answer('Добавте теги')


@dp.message_handler(state=OrderQuote.waiting_for_quote_tags)
async def tags_quote(message: types.Message, state: FSMContext):
    await state.update_data(tags=[Tag(tag=tag) for tag in message.text.split()])
    data = await state.get_data()
    add_quote_in_db(message.from_user.id, **data)
    await state.finish()
    await message.answer('Готово')


@dp.message_handler(Command('quick_add_quote'))
async def quick_add_quote(message: types.Message):
    data = message_destructor(message.text)
    add_quote_in_db(message.from_user.id, **data)
    await message.answer('Готово')


@dp.message_handler(state=OrderQuote)
async def next_step(message: types.Message, state: FSMContext):
    await OrderQuote.next()
