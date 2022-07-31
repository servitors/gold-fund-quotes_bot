from aiogram.utils import callback_data
import aiogram


confirm_add_quote_cb = callback_data.CallbackData('add_quote', 'action')
confirm_add_quote_keyboard = aiogram.types.InlineKeyboardMarkup()

confirm_add_quote_keyboard.add(aiogram.types.InlineKeyboardButton(
    text='YES',
    callback_data=confirm_add_quote_cb.new(action='confirm'))
)

confirm_add_quote_keyboard.add(aiogram.types.InlineKeyboardButton(
    text='NO',
    callback_data=confirm_add_quote_cb.new(action='cancel'))
)
