from aiogram.dispatcher import middlewares
from aiogram import dispatcher
import aiogram

from src.utils import db_api


class LimitQuotesMiddleware(middlewares.BaseMiddleware):

    def __init__(self):
        super(LimitQuotesMiddleware, self).__init__()
        self.quote_limit = 250

    async def on_process_message(self, message: aiogram.types.Message, data: dict):
        handler = dispatcher.handler.current_handler.get() or (lambda x: x)
        if getattr(handler, 'label', None) and db_api.count_quote(message.from_user.id) >= self.quote_limit:
            await message.answer('<b>You have run out of space.!</b>\n'
                                 'Buy additional slots or free up old ones',
                                 parse_mode=aiogram.types.ParseMode.HTML)
            raise dispatcher.handler.CancelHandler()
        return data
