from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import callback_data
import aiogram.types
import aiogram

from keyboards.buttons import quote_buttons, navigate_buttons
import keyboards.inline.callback_data
from utils.db_api import schemas


class QuoteMenuKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, quote_id: int):
        super(QuoteMenuKeyboard, self).__init__(row_width=2)
        self.quote_id = quote_id
        self.add(quote_buttons.EditQuoteTextButton(quote_id))
        self.add(quote_buttons.EditQuoteTextButton(quote_id),
                 quote_buttons.EditQuoteAuthorButton(quote_id))
        self.add(quote_buttons.QuoteTagsButton(quote_id))


class EditQuoteKeyboard(InlineKeyboardMarkup):

    def __init__(self, quote_id, page):
        super(EditQuoteKeyboard, self).__init__(row_width=2)
        self.quote_id = quote_id
        self.page = page
        self.add(*self.quote_buttons)
        self.add(self.back_button)

    @property
    def quote_buttons(self):
        return (
            InlineKeyboardButton(text='Изменить цитату', callback_data=quote_cb.new(
                action='edit_content',
                id=self.quote_id)),
            InlineKeyboardButton(text='Изменить автора', callback_data=quote_cb.new(
                action='edit_author',
                id=self.quote_id)),
            InlineKeyboardButton(text='Теги', callback_data=quote_cb.new(
                action='tags',
                id=self.quote_id))
        )

    @property
    def back_button(self):
        return InlineKeyboardButton(
            text='Назад',
            callback_data=QuoteMenuKeyboard.navigation_buttons_cb.new(
                action='navigate', page=self.page)
        )


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
