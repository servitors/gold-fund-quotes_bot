from loader import dp
from middlewares.limit_quotes import LimitQuotesMiddleware
from middlewares.throttling import ThrottlingMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(LimitQuotesMiddleware())
