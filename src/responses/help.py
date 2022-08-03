import aiogram.types

from src.responses import base


class HelpResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message):
        self.message = message

    async def _send_response(self):
        await self.message.answer(
            '/start - Start bot\n'
            '/help - This message\n'
            '/add_quote - Add quote\n'
            '$$ - Quickly Add quote\n'
            '(The author is marked with @, tags - #)'
        )
