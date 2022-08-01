from aiogram.utils import callback_data
import aiogram

import keyboards.inline.callback_factories


class TagMenuKeyboard(aiogram.types.InlineKeyboardMarkup):

    navigation_buttons_cb = callback_data.CallbackData('tag', 'action', 'page')

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

    def generate_quote_buttons(self) -> list[aiogram.types.InlineKeyboardButton]:
        return [
            aiogram.types.InlineKeyboardButton(
                text=tag.name,
                callback_data=keyboards.inline.callback_data.tag_cb.new(action=self.action, id=tag.order_in_user))
            for tag in self.tags
        ]

    def generate_navigation_buttons(self):
        return [
            aiogram.types.InlineKeyboardButton(
                text='Previous',
                callback_data=self.navigation_buttons_cb.new(page=self.page-1, action='navigate')),
            aiogram.types.InlineKeyboardButton(
                text='Next',
                callback_data=self.navigation_buttons_cb.new(page=self.page+1, action='navigate'))

        ]
