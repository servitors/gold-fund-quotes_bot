from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboards.inline.callback_data import tag_cb


class TagMenuKeyboard(InlineKeyboardMarkup):

    navigation_buttons_cb = CallbackData('tag', 'action', 'page')

    def __init__(self, tags, page, action):
        super(TagMenuKeyboard, self).__init__(row_width=3)
        self.tags = tags
        self.page = page
        self.action = action
        self.fill_keyboard()

    def fill_keyboard(self):
        self.add(
            *self.generate_quote_buttons()
        )
        self.add(
            *self.generate_navigation_buttons()
        )

    def generate_quote_buttons(self) -> list[InlineKeyboardButton]:
        return [
            InlineKeyboardButton(
                text=tag.content,
                callback_data=tag_cb.new(action=self.action, id=tag.order_in_user))
            for tag in self.tags
        ]

    def generate_navigation_buttons(self):
        return [
            InlineKeyboardButton(
                text='Previous',
                callback_data=self.navigation_buttons_cb.new(page=self.page-1, action='navigate')),
            InlineKeyboardButton(
                text='Next',
                callback_data=self.navigation_buttons_cb.new(page=self.page+1, action='navigate'))

        ]
