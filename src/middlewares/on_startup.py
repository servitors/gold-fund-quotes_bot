from aiogram import dispatcher

from src.middlewares import limit_quotes


def on_startup(dp: dispatcher.Dispatcher):
    dp.middleware.setup(limit_quotes.LimitQuotesMiddleware())
