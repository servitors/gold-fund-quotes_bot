from aiogram import types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import ParseMode

from utils.db_api import count_quote


class LimitQuotesMiddleware(BaseMiddleware):

    def __init__(self):
        super(LimitQuotesMiddleware, self).__init__()
        self.quote_limit = 250

    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get() or (lambda x: x)
        if getattr(handler, 'label', None) and count_quote(message.from_user.id) >= self.quote_limit:
            await message.answer('<b>You have run out of space.!</b>\n'
                                 'Buy additional slots or free up old ones',
                                 parse_mode=ParseMode.HTML)
            raise CancelHandler()
        return data
