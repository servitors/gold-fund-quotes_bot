from aiogram.dispatcher import filters
import aiogram.types

from keyboards.inline import callback_factories
import utils.db_api.session
from utils import db_api
from loader import dp
import responses.tag


@dp.message_handler(filters.Command('tag_menu'))
async def tag_menu(message: aiogram.types.Message):
    user_id = message.from_user.id
    with db_api.session.Session() as session, session.begin():
        tags = db_api.get_user_tags(session, user_id, page=0, page_size=9)
    menu = tag_menu.TagMenuKeyboard(tags, page=0, action='select')
    await message.answer(text='Tag Menu', reply_markup=menu)


@dp.callback_query_handler(callback_factories.TagsCallbackFactory().filter())
async def navigate_tag_menu(query: aiogram.types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    page = int(callback_data['page'])
    with db_api.session.Session() as session, session.begin():
        quotes = db_api.get_user_tags(session, user_id, page=page, page_size=9)
    await responses.tag.TagsResponse(query, quotes, page)
