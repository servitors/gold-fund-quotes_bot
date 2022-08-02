from aiogram.dispatcher.filters import state


class AddQuote(state.StatesGroup):
    waiting_for_quote_content = state.State()
    waiting_for_quote_author = state.State()
    waiting_for_quote_tags = state.State()
