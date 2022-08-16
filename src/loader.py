import aiogram
from aiogram.contrib.fsm_storage import memory

import settings


bot = aiogram.Bot(token=settings.BOT_TOKEN)
storage = memory.MemoryStorage()
dp = aiogram.Dispatcher(bot, storage=storage)
