import aiogram.types

from keyboards.inline import quote_keyboards
from utils.db_api import schemas
from responses import base
import utils.quote


class QuoteMenuResponse(base.BaseResponse):
    def __init__(self, callback: aiogram.types.CallbackQuery, quote: schemas.Quote):
        self.__callback = callback
        self.__quote = quote

    async def _send_response(self):
        keyboard = quote_keyboards.QuoteMenuKeyboard(quote_id=self.__quote.id)
        await self.__callback.message.edit_text(
            utils.quote.quote_constructor(
                self.__quote.content, self.__quote.author))
        await self.__callback.message.edit_reply_markup(keyboard)
