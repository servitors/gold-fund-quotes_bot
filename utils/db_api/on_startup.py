from .engine import engine
from .base import Base


def on_startup():
    Base.metadata.create_all(engine)
