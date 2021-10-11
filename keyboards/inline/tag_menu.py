from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


class TagMenuKeyboard:

    quote_menu_cb = CallbackData('tag', 'id')
    navigation_buttons_cb = CallbackData('tag_menu', 'page')

    def __init__(self, tags, page):
        self.tags = tags
        self.page = page
        self.keyboard = InlineKeyboardMarkup()
        self.fill_keyboard()

    def fill_keyboard(self):
        self.keyboard.add(
            *self.generate_quote_buttons()
        )
        self.keyboard.add(
            *self.generate_navigation_buttons()
        )

    def generate_quote_buttons(self) -> list[InlineKeyboardButton]:
        return [
            InlineKeyboardButton(
                text=tag.content,
                callback_data=self.quote_menu_cb.new(id=tag.id))
            for tag in self.tags
        ]

    def generate_navigation_buttons(self):
        return [
            InlineKeyboardButton(
                text='Previous',
                callback_data=self.navigation_buttons_cb.new(page=self.page-1)),
            InlineKeyboardButton(
                text='Next',
                callback_data=self.navigation_buttons_cb.new(page=self.page+1))

        ]
