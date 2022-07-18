from sqlalchemy import create_engine

__all__ = ("engine",)


engine = create_engine(config.DATABASE_URI)
