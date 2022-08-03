from aiogram.dispatcher import filters
from aiogram import dispatcher
import aiogram.types

from utils import db_api
from utils.db_api import schemas
from states import quote_states
from loader import dp
import utils.quote


def quote_limit():
    def decorator(func):
        setattr(func, 'label', True)
        return func

    return decorator


@quote_limit()
@dp.message_handler(filters.Command('add_quote'))
async def add_quote_command(message: aiogram.types.Message):
    await quote_states.AddQuote.waiting_for_quote_content.set()
    await message.answer('Input quote')


@dp.message_handler(state=quote_states.AddQuote.waiting_for_quote_content)
async def content_quote(message: aiogram.types.Message, state: dispatcher.FSMContext):
    await state.update_data(content=message.text)
    await quote_states.AddQuote.next()
    await message.answer('Input author')


@dp.message_handler(state=quote_states.AddQuote.waiting_for_quote_author)
async def author_quote(message: aiogram.types.Message, state: dispatcher.FSMContext):
    await state.update_data(author=message.text)
    await quote_states.AddQuote.next()
    await message.answer('Input tags')


@dp.message_handler(state=quote_states.AddQuote.waiting_for_quote_tags)
async def tags_quote(message: aiogram.types.Message, state: dispatcher.FSMContext):
    await state.update_data(tag=[
        schemas.Tag(
            name=tag,
            user_id=message.from_user.id,
            order_in_user=db_api.count_tags(message.from_user.id))
        for tag in message.text.split()
    ])
    data = await state.get_data()
    db_api.add_quote_in_db(message.from_user.id, **data)
    await message.answer('Done')
    await message.delete()
    await state.finish()


@quote_limit()
@dp.message_handler(filters.Text(startswith='$$'))
async def quick_add_quote(message: aiogram.types.Message):
    data = utils.quote.quote_destructor(message.text)
    if data:
        db_api.add_quote_in_db(message.from_user.id, **data)
        await message.answer('Done')
    else:
        await message.answer('Message must not be empty')
