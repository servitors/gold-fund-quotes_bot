from aiogram.dispatcher.filters.state import StatesGroup, State


class OrderQuote(StatesGroup):
    waiting_for_quote_content = State()
    waiting_for_quote_author = State()
    waiting_for_quote_tags = State()
    finish = State()


