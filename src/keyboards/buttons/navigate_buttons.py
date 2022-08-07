import aiogram.types
from aiogram.utils import callback_data


class PreviousButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, callback_factory: callback_data.CallbackData, page: int):
        super().__init__('Previous', callback_data=callback_factory.new(page=page))


class NextPreviousButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, callback_factory: callback_data.CallbackData, page: int):
        super().__init__('Next', callback_data=callback_factory.new(page=page))
