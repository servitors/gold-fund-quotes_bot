from functools import lru_cache

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from keyboards.inline.confirm_add_quote import confirm_add_quote_keyboard, confirm_add_quote_cb
from loader import dp
from states.order_quote import *
from utils.db_api import add_quote_in_db, Tag, count_tags
from utils.misc.messages import *

OPTIONAL_FIELDS = (OrderQuote.waiting_for_quote_tags,)


def quote_limit():
    def decorator(func):
        setattr(func, 'label', True)
        return func

    return decorator


async def get_step_by_state(state: FSMContext) -> str:
    return get_add_quote_steps()[await state.get_state()]


@lru_cache
def get_add_quote_steps():
    step_names = ('Введите цитату', 'Укажите автора', 'Добавьте теги', 'Готово')
    return dict(zip(OrderQuote.states_names, step_names))


@dp.message_handler(Command('skip'), state=OPTIONAL_FIELDS)
async def skip_step(message: types.Message, state: FSMContext):
    await OrderQuote.next()
    if await state.get_state() == await OrderQuote.last():
        await message.answer(text="Ok?", reply_markup=confirm_add_quote_keyboard)
    else:
        await message.answer(await get_step_by_state(state))


@dp.message_handler(Command('add_quote'))
@quote_limit()
async def add_quote_command(message: types.Message):
    await OrderQuote.waiting_for_quote_content.set()
    await message.answer('Введите цитату')


@dp.message_handler(state=OrderQuote.waiting_for_quote_content)
async def content_quote(message: types.Message, state: FSMContext):
    await state.update_data(content=message.text)
    await OrderQuote.next()
    await message.answer(await get_step_by_state(state))


@dp.message_handler(state=OrderQuote.waiting_for_quote_author)
async def author_quote(message: types.Message, state: FSMContext):
    await state.update_data(author=message.text)
    await OrderQuote.next()
    await message.answer(await get_step_by_state(state))


@dp.message_handler(state=OrderQuote.waiting_for_quote_tags)
async def tags_quote(message: types.Message, state: FSMContext):
    await state.update_data(tag=[
        Tag(
            name=tag,
            user_id=message.from_user.id,
            order_in_user=count_tags(message.from_user.id))
        for tag in message.text.split()
    ])
    await OrderQuote.next()
    await message.answer(text="Ok?", reply_markup=confirm_add_quote_keyboard)


@dp.callback_query_handler(confirm_add_quote_cb.filter(), state=OrderQuote.finish)
async def finish_add_quote(query: types.CallbackQuery, state: FSMContext):
    if 'confirm' in query.data:
        data = await state.get_data()
        add_quote_in_db(query.from_user.id, **data)
        await query.message.answer(await get_step_by_state(state))
    else:
        await query.message.answer('Отменено')
    await query.message.delete()
    await state.finish()
    await query.answer()


@quote_limit()
@dp.message_handler(Text(startswith='$$'))
async def quick_add_quote(message: types.Message):
    data = message_destructor(message.text)
    if data:
        add_quote_in_db(message.from_user.id, **data)
        await message.answer('Готово')
    else:
        await message.answer('Сообщение не должно быть пустым!')
