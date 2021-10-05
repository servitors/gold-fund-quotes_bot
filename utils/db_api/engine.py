from sqlalchemy import create_engine

import data.config as config


__all__ = ("engine",)


engine = create_engine(config.DATABASE_URI)
