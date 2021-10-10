from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start bot"),
            types.BotCommand("help", "Display help"),
            types.BotCommand("/add_quote", "Add new quote"),
            types.BotCommand("/quick_add_quote", "Add new quote quickly"),
            types.BotCommand('/cancel', 'Cancel operation'),
            types.BotCommand('/skip', 'Skip one step'),
            types.BotCommand('/quote_menu', 'Show quote menu'),
        ]
    )
