from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start bot"),
            types.BotCommand("help", "Display help"),
            types.BotCommand("/add_quote", "Add new quote"),
            types.BotCommand('/cancel', 'Cancel operation'),
            types.BotCommand('/skip', 'Skip one step'),
            types.BotCommand('/quote_menu', 'Show quote menu'),
            types.BotCommand('/tag_menu', 'Show tag menu'),
        ]
    )
