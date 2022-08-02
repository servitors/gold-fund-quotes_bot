from aiogram.utils import callback_data


class QuoteCallbackFactory(callback_data.CallbackData):
    def __init__(self):
        super().__init__('quote', 'action', 'id')


class TagCallbackFactory(callback_data.CallbackData):
    def __init__(self):
        super().__init__('tag', 'action', 'id')


class QuotesCallbackFactory(callback_data.CallbackData):
    def __init__(self):
        super().__init__('quote_menu', 'page')


class TagMenuCallbackFactory(callback_data.CallbackData):
    def __init__(self):
        super().__init__('tag_menu', 'page')
