from loader import dp
from middlewares.limit_quotes import LimitQuotesMiddleware
from middlewares.throttling import ThrottlingMiddleware


def on_startup():
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(LimitQuotesMiddleware())
