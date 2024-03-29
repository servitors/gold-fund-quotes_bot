import aiogram.types
from aiogram import dispatcher
from aiogram.dispatcher import filters

import utils.quote
from filters import is_quote
from loader import dp
from services import db_api
from services.db_api import schemas
from states import quote_states


def quote_limit():
    def decorator(func):
        setattr(func, 'label', True)
        return func

    return decorator


@quote_limit()
@dp.message_handler(filters.Command('add_quote'))
async def add_quote_command(message: aiogram.types.Message):
    await quote_states.AddQuote.waiting_for_quote_content.set()
    await message.answer('Enter quote')


@dp.message_handler(state=quote_states.AddQuote.waiting_for_quote_content)
async def quote_content(message: aiogram.types.Message, state: dispatcher.FSMContext):
    await state.update_data(content=message.text)
    await quote_states.AddQuote.next()
    await message.answer('Enter author')


@dp.message_handler(state=quote_states.AddQuote.waiting_for_quote_author)
async def quote_author(message: aiogram.types.Message, state: dispatcher.FSMContext):
    await state.update_data(author=message.text)
    await quote_states.AddQuote.next()
    await message.answer('Enter tags')


@dp.message_handler(state=quote_states.AddQuote.waiting_for_quote_tags)
async def quote_tags(message: aiogram.types.Message, state: dispatcher.FSMContext):
    tags = [schemas.Tag(name=tag, user_id=message.from_user.id)
            for tag in message.text.split()]
    data = await state.get_data()
    with db_api.create_session() as session:
        db_api.add_quote_to_db(session, message.from_user.id, **data)
    await message.answer('✅ Success!')
    await state.finish()


@quote_limit()
@dp.message_handler(is_quote.QuoteFilter())
async def quick_add_quote(message: aiogram.types.Message):
    quote, author, tags = utils.quote.quote_destructor(message.text)
    with db_api.create_session() as session:
        db_api.add_quote_to_db(session, message.from_user.id, content=quote, auhtor=author, tags=tags)
    await message.answer('✅ Success!')
