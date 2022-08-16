from sqlalchemy import orm

from services.db_api import engine

Session = orm.sessionmaker(bind=engine.engine)
