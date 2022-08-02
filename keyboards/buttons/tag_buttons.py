import aiogram.types

from keyboards.inline import callback_factories


class TagButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, text: str, page: int):
        callback_factory = callback_factories.TagsCallbackFactory()
        super().__init__(text, callback_data=callback_factory.new(page=page))
