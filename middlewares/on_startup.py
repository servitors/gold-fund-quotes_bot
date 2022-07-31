from middlewares import limit_quotes
import loader


def on_startup():
    loader.dp.middleware.setup(limit_quotes.LimitQuotesMiddleware())
