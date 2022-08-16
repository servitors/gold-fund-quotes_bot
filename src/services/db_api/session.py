import contextlib
import typing

from sqlalchemy import orm

from services.db_api import engine


RawSession = orm.sessionmaker(bind=engine.engine)


@contextlib.contextmanager
def create_session() -> typing.Generator[orm.Session, None, None]:
    with RawSession() as session, session.begin():
        yield session
