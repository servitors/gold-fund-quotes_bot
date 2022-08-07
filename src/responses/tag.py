import aiogram.types

from keyboards.inline import tag_keyboards
from utils.db_api import schemas
from responses import base


class TagsResponse(base.BaseResponse):
    def __init__(self, update: aiogram.types.CallbackQuery | aiogram.types.Message,
                 tags: list[schemas.Tag], page: int):
        self.__update = update
        self.__tags = tags
        self.__page = page

    async def _send_response(self):
        if isinstance(self.__update, aiogram.types.CallbackQuery):
            await self.__update.message.edit_text('Update')
            await self.__update.message.edit_reply_markup(
                tag_keyboards.TagsKeyboard(self.__tags, self.__page)
            )
            await self.__update.answer()
