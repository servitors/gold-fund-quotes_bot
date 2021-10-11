from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.inline.pagination import Pagination
from keyboards.inline.tag_menu import TagMenuKeyboard
from loader import dp
from utils.db_api import get_user_tags, count_tags


@dp.message_handler(Command('tag_menu'))
async def tag_menu(message: types.Message):
    user_id = message.from_user.id
    tags = get_user_tags(user_id, range(0, min(10, count_tags(user_id))))
    menu = TagMenuKeyboard(tags, page=0)
    await message.answer(text='Tag Menu', reply_markup=menu.keyboard)


@dp.callback_query_handler(TagMenuKeyboard.navigation_buttons_cb.filter())
async def navigate_tag_menu(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    quantity = count_tags(user_id)
    elements_on_page = 9
    if quantity > elements_on_page:
        pagination = Pagination(quantity, int(callback_data['page']), elements_on_page)
        quotes = get_user_tags(user_id, pagination.range_elements)
        menu = TagMenuKeyboard(quotes, page=pagination.page)
        await query.message.edit_reply_markup(reply_markup=menu.keyboard)
    await query.answer()
