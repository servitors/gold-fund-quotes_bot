from sqlalchemy import create_engine

from data.config import config


__all__ = ("engine",)


engine = create_engine(config.DATABASE_URI)
