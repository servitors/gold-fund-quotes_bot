import aiogram


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            aiogram.types.BotCommand("start", "Start bot"),
            aiogram.types.BotCommand("help", "Display help"),
            aiogram.types.BotCommand("add_quote", "Add new quote"),
            aiogram.types.BotCommand('cancel', 'Cancel operation'),
            aiogram.types.BotCommand('skip', 'Skip one step'),
            aiogram.types.BotCommand('quote_menu', 'Show quote menu'),
            aiogram.types.BotCommand('tag_menu', 'Show tag menu'),
        ]
    )
