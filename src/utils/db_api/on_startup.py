from src.utils.db_api import engine, base


def on_startup():
    base.Base.metadata.create_all(engine.engine)
