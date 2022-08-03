import aiogram

from keyboards.buttons import tag_buttons, navigate_buttons
from keyboards.inline import callback_factories
from utils.db_api import schemas


class TagsKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, tags: list[schemas.Tag], page: int):
        super().__init__()
        self.__tags = tags
        self.__page = page
        self.add(*[tag_buttons.TagButton(tag.name, tag.id) for tag in self.__tags])
        callback_factory = callback_factories.QuoteMenuCallbackFactory()
        self.row(
            navigate_buttons.PreviousButton(callback_factory=callback_factory, page=self.__page - 1),
            navigate_buttons.NextPreviousButton(callback_factory=callback_factory, page=self.__page + 1)
        )
