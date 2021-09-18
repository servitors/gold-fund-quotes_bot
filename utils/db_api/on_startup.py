from .engine import engine
from .base import Base


def on_startup(dispatcher):
    Base.metadata.create_all(engine)