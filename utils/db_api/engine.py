import sqlalchemy

from config import settings


__all__ = ("engine",)

engine = sqlalchemy.create_engine(settings.DATABASE_URI)
