from typing import Union

from sqlalchemy.dialects.postgresql import insert

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .schemas import *
from .engine import engine


def add_user_in_db(id: int, name: str) -> bool:
    statement = insert(User).values(id=id, name=name)
    statement = statement.on_conflict_do_nothing(index_elements=[User.id])
    with Session(engine) as session:
        try:
            session.execute(statement)
        except IntegrityError:
            return False
        else:
            session.commit()
            return True


def add_quote_in_db(user_id: int, **kwargs) -> None:
    with Session(engine) as session:
        session.add(Quote(user_id=user_id, **kwargs))
        session.commit()


def add_tag_in_db(tag:str) -> None:
    with Session(engine) as session:
        session.add(Tag(tag=tag))
        session.commit()


def get_user_by_id(user_id: int) -> User:
    with Session(engine) as session:
        return session.query(User).filter_by(id=user_id).one()


def get_quotes_by_tags(user_id: int, tags: list[str]) -> list[Union[None, Quote]]:
    with Session(engine) as session:
        if tags:
            tags = session.query(Tag).filter(Tag.tag.in_(tags)).all()
            return session.query(Quote).filter_by(user_id=user_id, tags=tags).all()

        return list()


def get_user_tags(user_id: int) -> list[Union[None, Quote]]:
    with Session(engine) as session:
        return session.query(Tag).filter_by(user_id=user_id).all()


def update_quote(quote_id: int, **kwargs) -> None:
    with Session(engine) as session:
        session.query(Quote).filter_by(id=quote_id).update(kwargs)


def delete_quote(quote_id: int) -> None:
    with Session(engine) as session:
        session.query(Quote).filter_by(id=quote_id).delete()


def delete_tag(tag_id: int) -> None:
    with Session(engine) as session:
        session.query(Tag).filter_by(id=tag_id).delete()