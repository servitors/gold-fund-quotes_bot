import aiogram.types

from keyboards.inline import quote_keyboards
from services.db_api import schemas
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


class QuotesResponse(base.BaseResponse):
    def __init__(self, update: aiogram.types.CallbackQuery | aiogram.types.Message,
                 quotes: list[schemas.Quote], page: int = 0):
        self.__update = update
        self.__page = page
        self.__quotes = quotes

    async def _send_response(self):
        if isinstance(self.__update, aiogram.types.CallbackQuery):
            await self.__update.message.edit_text('Quotes')
            await self.__update.message.edit_reply_markup(
                quote_keyboards.QuotesKeyboard(self.__quotes, page=self.__page)
            )
        elif isinstance(self.__update, aiogram.types.Message):
            await self.__update.answer(
                'Quotes', reply_markup=quote_keyboards.QuotesKeyboard(self.__quotes, self.__page)
            )
