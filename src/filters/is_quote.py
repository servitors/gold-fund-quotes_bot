import aiogram.types
from aiogram.dispatcher import filters


class QuoteFilter(filters.BoundFilter):
    async def check(self, message: aiogram.types.Message) -> bool:
        text = message.text
        return text.startswith('"') and text.count('"') > 2
