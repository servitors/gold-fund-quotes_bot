from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

confirm_add_quote_cb = CallbackData('add_quote', 'action')
confirm_add_quote_keyboard = InlineKeyboardMarkup()

confirm_add_quote_keyboard.add(InlineKeyboardButton(
    text='YES',
    callback_data=confirm_add_quote_cb.new(action='confirm'))
)

confirm_add_quote_keyboard.add(InlineKeyboardButton(
    text='NO',
    callback_data=confirm_add_quote_cb.new(action='cancel'))
)
