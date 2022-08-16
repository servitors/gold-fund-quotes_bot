from sqlalchemy import orm

from services.db_api import engine

RawSession = orm.sessionmaker(bind=engine.engine)
