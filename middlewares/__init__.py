from aiogram import Dispatcher

from loader import dp
from .limit_quotes import LimitQuotesMiddleware
from .throttling import ThrottlingMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(LimitQuotesMiddleware())
