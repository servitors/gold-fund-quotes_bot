from aiogram.utils import callback_data
import aiogram.types

import keyboards.inline.callback_data
from utils.db_api import schemas


class QuoteMenuKeyboard(aiogram.types.InlineKeyboardMarkup):

    navigation_buttons_cb = callback_data.CallbackData('quote', 'action', 'page')

    def __init__(self, quotes: list[schemas.Quote], page: int, action: str):
        super(QuoteMenuKeyboard, self).__init__(row_width=2)
        self.quotes = quotes
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
                text=quote.content,
                callback_data=keyboards.inline.callback_data.quote_cb.new(
                    action=self.action, id=quote.order_in_user)
            )
            for quote in self.quotes
        ]

    def generate_navigation_buttons(self) -> list[aiogram.types.InlineKeyboardButton]:
        return [
            aiogram.types.InlineKeyboardButton(
                text='Previous',
                callback_data=self.navigation_buttons_cb.new(page=self.page - 1, action='navigate')),
            aiogram.types.InlineKeyboardButton(
                text='Next',
                callback_data=self.navigation_buttons_cb.new(page=self.page + 1, action='navigate'))

        ]
