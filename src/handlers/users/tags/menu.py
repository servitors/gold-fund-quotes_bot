from aiogram.dispatcher import filters
import aiogram.types

from keyboards.inline import callback_factories
import utils.db_api.session
from utils import db_api
import utils.pagination
from loader import dp


@dp.message_handler(filters.Command('tag_menu'))
async def tag_menu(message: aiogram.types.Message):
    user_id = message.from_user.id
    with db_api.session.Session() as session, session.begin():
        tags = db_api.get_user_tags_in_range(session, user_id, range(0, 10))
    menu = tag_menu.TagMenuKeyboard(tags, page=0, action='select')
    await message.answer(text='Tag Menu', reply_markup=menu)


@dp.callback_query_handler(callback_factories.TagsCallbackFactory().filter())
async def navigate_tag_menu(query: aiogram.types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    with db_api.session.Session() as session, session.begin():
        quantity = db_api.count_tags(session, user_id)
    elements_on_page = 9
    if quantity > elements_on_page:
        pagination = utils.pagination.Pagination(quantity, int(callback_data['page']), elements_on_page)
        with db_api.session.Session() as session, session.begin():
            quotes = db_api.get_user_tags_in_range(session, user_id, pagination.range_elements)
        menu = tag_menu.TagMenuKeyboard(quotes, page=pagination.__page, action='select')
        await query.message.edit_reply_markup(reply_markup=menu)
    await query.answer()
