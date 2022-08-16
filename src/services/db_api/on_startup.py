from services.db_api import base
from services.db_api import engine


def on_startup():
    base.Base.metadata.create_all(engine.engine)
