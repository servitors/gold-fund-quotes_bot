import aiogram

from keyboards.buttons import quote_buttons, navigate_buttons
from keyboards.inline import callback_factories
from utils.db_api import schemas


class QuoteMenuKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, quote_id: int):
        super(QuoteMenuKeyboard, self).__init__(row_width=2)
        self.quote_id = quote_id
        self.add(quote_buttons.EditQuoteTextButton(quote_id))
        self.add(quote_buttons.EditQuoteTextButton(quote_id),
                 quote_buttons.EditQuoteAuthorButton(quote_id))
        self.add(quote_buttons.QuoteTagsButton(quote_id))


class QuotesKeyboard(aiogram.types.InlineKeyboardMarkup):
    def __init__(self, quotes: list[schemas.Quote], page: int):
        super().__init__()
        self.__quotes = quotes
        self.__page = page
        self.add(*[quote_buttons.QuoteButton(quote.content, quote.id) for quote in self.__quotes])
        callback_factory = callback_factories.QuoteMenuCallbackFactory()
        self.row(
            navigate_buttons.PreviousButton(callback_factory=callback_factory, page=self.__page - 1),
            navigate_buttons.NextPreviousButton(callback_factory=callback_factory, page=self.__page + 1)
        )
