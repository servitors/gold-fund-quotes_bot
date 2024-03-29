import aiogram.types

from keyboards.inline import callback_factories


class TagButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, text: str, tag_id: int):
        callback_factory = callback_factories.TagMenuCallbackFactory()
        super().__init__(text, callback_data=callback_factory.new(action='select', id=tag_id))
