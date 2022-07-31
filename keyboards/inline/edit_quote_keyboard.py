from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_data import quote_cb
from keyboards.inline import quote_menu


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
            callback_data=quote_menu.QuoteMenuKeyboard.navigation_buttons_cb.new(
                action='navigate', page=self.page)
        )
