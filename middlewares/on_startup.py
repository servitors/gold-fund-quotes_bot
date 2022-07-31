from aiogram import dispatcher

from middlewares import limit_quotes


def on_startup(dp: dispatcher.Dispatcher):
    dp.middleware.setup(limit_quotes.LimitQuotesMiddleware())
