import aiogram.types

from keyboards.inline import quote_keyboards
from responses import base


class QuoteMenuResponse(base.BaseResponse):
    def __init__(self, callback: aiogram.types.CallbackQuery, quote_id: int):
        self.__callback = callback
        self.__quote_id = quote_id

    async def _send_response(self):
        keyboard = quote_keyboards.QuoteMenuKeyboard(quote_id=self.__quote_id)
        await self.__callback.message.answer('Quote Menu', reply_markup=keyboard)
