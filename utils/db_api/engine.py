from sqlalchemy import create_engine

from config import settings


__all__ = ("engine",)


engine = create_engine(settings.DATABASE_URI)
