from aiogram.utils import executor

from utils import db_api, set_default_commands
import middlewares
import handlers


async def on_startup(dispatcher):
    db_api.on_startup()
    middlewares.on_startup()
    await set_default_commands.set_default_commands(dispatcher)

if __name__ == '__main__':
    executor.start_polling(handlers.dp, on_startup=on_startup, skip_updates=True)
