from aiogram import types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import ParseMode

from utils.db_api import count_quote


class LimitQuotesMiddleware(BaseMiddleware):

    def __init__(self):
        super(LimitQuotesMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get() or (lambda x: x)
        # print(getattr(handler, 'label', None))
        print(count_quote(message.from_user.id))
        if getattr(handler, 'label', None) and count_quote(message.from_user.id) >= 250:
            await message.answer('<b>У вас закончилось место!</b>\n'
                                 'Купите дополнительные слоты или освободите старые',
                                 parse_mode=ParseMode.HTML)
            raise CancelHandler()
