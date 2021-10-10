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
        session.add(Quote(user_id=user_id, order_in_user=count_quote(user_id), **kwargs))
        session.commit()


def add_tag_in_db(name: str, user_id: int) -> None:
    with Session(engine) as session:
        session.add(Tag(name=name, user_id=user_id))
        session.commit()


def get_user_by_id(user_id: int) -> User:
    with Session(engine) as session:
        return session.query(User).filter_by(id=user_id).one()


def get_quotes_by_tags(user_id: int, tags: list[str]) -> list[Union[None, Quote]]:
    with Session(engine) as session:
        quotes = get_user_quotes(user_id)
        if tags:
            return [quote for quote in quotes if sorted([tag.name for tag in quote.tag]) == sorted(tags)]
        else:
            return quotes


def get_user_quotes(user_id: int, range_id: range) -> list[Union[None, Quote]]:
    with Session(engine) as session:
        if range_id:
            return [
                quote for quote in session.query(Quote).filter(
                    Quote.user_id == user_id,
                    Quote.order_in_user.in_(range_id)
                )
            ]
        return [quote for quote in session.query(Quote).filter(Quote.user_id == user_id)]


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


def count_quote(user_id):
    with Session(engine) as session:
        return session.query(Quote).filter_by(user_id=user_id).count()
