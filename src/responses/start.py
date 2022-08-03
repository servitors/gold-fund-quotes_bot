import aiogram.types

from src.responses import base


class StartResponse(base.BaseResponse):
    def __init__(self, message: aiogram.types.Message, user_full_name: str):
        self.message = message
        self.user_full_name = user_full_name

    async def _send_response(self):
        await self.message.answer(f'Hello, {self.user_full_name}!')
