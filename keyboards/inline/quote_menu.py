from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


class QuoteMenuKeyboard:

    quote_menu_cb = CallbackData('quote', 'id')
    navigation_buttons_cb = CallbackData('quote', 'page')

    def __init__(self, quotes, page):
        self.quotes = quotes
        self.page = page
        self.keyboard = InlineKeyboardMarkup(row_width=2)
        self.fill_keyboard()

    def fill_keyboard(self):
        self.keyboard.add(
            *self.generate_quote_buttons()
        )
        self.keyboard.add(
            *self.generate_navigation_buttons(self.page)
        )

    def generate_quote_buttons(self) -> list[InlineKeyboardButton]:
        return [
            InlineKeyboardButton(
                text=quote.content,
                callback_data=self.quote_menu_cb.new(id=quote.id))
            for quote in self.quotes
        ]

    def generate_navigation_buttons(self, page):
        return [
            InlineKeyboardButton(
                text='Previous',
                callback_data=self.navigation_buttons_cb.new(page=page-1)),
            InlineKeyboardButton(
                text='Next',
                callback_data=self.navigation_buttons_cb.new(page=page+1))

        ]
