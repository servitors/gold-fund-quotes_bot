from aiogram.dispatcher import filters
import aiogram.types

from keyboards.inline import tag_menu
from utils import db_api
import keyboards.inline.pagination
import loader


@loader.dp.message_handler(filters.Command('tag_menu'))
async def tag_menu(message: aiogram.types.Message):
    user_id = message.from_user.id
    tags = db_api.get_user_tags_in_range(user_id, range(0, 10))
    menu = tag_menu.TagMenuKeyboard(tags, page=0, action='select')
    await message.answer(text='Tag Menu', reply_markup=menu)


@loader.dp.callback_query_handler(tag_menu.TagMenuKeyboard.navigation_buttons_cb.filter(action='navigate'))
async def navigate_tag_menu(query: aiogram.types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    quantity = db_api.count_tags(user_id)
    elements_on_page = 9
    if quantity > elements_on_page:
        pagination = keyboards.inline.pagination.Pagination(quantity, int(callback_data['page']), elements_on_page)
        quotes = db_api.get_user_tags_in_range(user_id, pagination.range_elements)
        menu = tag_menu.TagMenuKeyboard(quotes, page=pagination.page, action='select')
        await query.message.edit_reply_markup(reply_markup=menu)
    await query.answer()
