from utils.db_api import base, engine


def on_startup():
    base.Base.metadata.create_all(engine.engine)
