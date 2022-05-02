from sqlalchemy import create_engine

from data.config import secrets


__all__ = ("engine",)


engine = create_engine(config.DATABASE_URI)
