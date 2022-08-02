import functools

from aiogram.dispatcher import filters
from aiogram import dispatcher
import aiogram.types

from keyboards.inline import confirm_add_quote
from utils import db_api, messages
from utils.db_api import schemas
from states import quote_states
from loader import dp


def quote_limit():
    def decorator(func):
        setattr(func, 'label', True)
        return func

    return decorator


@quote_limit()
@dp.message_handler(filters.Command('add_quote'))
async def add_quote_command(message: aiogram.types.Message):
    await quote.AddQuote.waiting_for_quote_content.set()
    await message.answer('Input quote')


@dp.message_handler(state=quote.AddQuote.waiting_for_quote_content)
async def content_quote(message: aiogram.types.Message, state: dispatcher.FSMContext):
    await state.update_data(content=message.text)
    await quote.AddQuote.next()
    await message.answer('Input author')


@dp.message_handler(state=quote.AddQuote.waiting_for_quote_author)
async def author_quote(message: aiogram.types.Message, state: dispatcher.FSMContext):
    await state.update_data(author=message.text)
    await quote.AddQuote.next()
    await message.answer('Input tags')


@dp.message_handler(state=quote.AddQuote.waiting_for_quote_tags)
async def tags_quote(message: aiogram.types.Message, state: dispatcher.FSMContext):
    await state.update_data(tag=[
        schemas.Tag(
            name=tag,
            user_id=message.from_user.id,
            order_in_user=db_api.count_tags(message.from_user.id))
        for tag in message.text.split()
    ])
    await quote.AddQuote.next()
    await message.answer(text="Ok?", reply_markup=confirm_add_quote.confirm_add_quote_keyboard)


@dp.callback_query_handler(confirm_add_quote.confirm_add_quote_cb.filter(),
                           state=quote.AddQuote.waiting_for_confirmation)
async def finish_add_quote(query: aiogram.types.CallbackQuery, state: dispatcher.FSMContext):
    if 'confirm' in query.data:
        data = await state.get_data()
        db_api.add_quote_in_db(query.from_user.id, **data)
        await query.message.answer('Done')
    else:
        await query.message.answer('Canceled')
    await query.message.delete()
    await state.finish()
    await query.answer()


@quote_limit()
@dp.message_handler(filters.Text(startswith='$$'))
async def quick_add_quote(message: aiogram.types.Message):
    data = messages.message_destructor(message.text)
    if data:
        db_api.add_quote_in_db(message.from_user.id, **data)
        await message.answer('Done')
    else:
        await message.answer('Message must not be empty')
