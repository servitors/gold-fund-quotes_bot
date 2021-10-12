from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboards.inline.callback_data import quote_cb
from utils.db_api import Quote


class QuoteMenuKeyboard(InlineKeyboardMarkup):

    navigation_buttons_cb = CallbackData('quote', 'action', 'page')

    def __init__(self, quotes: list[Quote], page: int, action: str):
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

    def generate_quote_buttons(self) -> list[InlineKeyboardButton]:
        return [
            InlineKeyboardButton(
                text=quote.content,
                callback_data=quote_cb.new(action=self.action, id=quote.order_in_user))
            for quote in self.quotes
        ]

    def generate_navigation_buttons(self) -> list[InlineKeyboardButton]:
        return [
            InlineKeyboardButton(
                text='Previous',
                callback_data=self.navigation_buttons_cb.new(page=self.page - 1, action='navigate')),
            InlineKeyboardButton(
                text='Next',
                callback_data=self.navigation_buttons_cb.new(page=self.page + 1, action='navigate'))

        ]
