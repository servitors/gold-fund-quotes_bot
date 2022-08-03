from aiogram.utils import executor

from utils import db_api
from src.misc import set_default_commands
from src import middlewares, handlers


async def on_startup(dispatcher):
    db_api.on_startup()
    middlewares.on_startup(handlers.dp)
    await set_default_commands.set_default_commands(dispatcher)

if __name__ == '__main__':
    executor.start_polling(handlers.dp, on_startup=on_startup, skip_updates=True)