import aiogram.types

from keyboards.inline import callback_factories


class EditQuoteAuthorButton(aiogram.types.InlineKeyboardButton):
    def __init__(self, quote_id: int):
        callback_factory = callback_factories.QuoteMenuCallbackFactory()
        super().__init__('Изменить автора', callback_data=callback_factory.new(
            action='edit', id=quote_id
        ))
