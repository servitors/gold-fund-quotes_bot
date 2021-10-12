from typing import Union

from sqlalchemy.dialects.postgresql import insert

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .base import Base
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
        session.add(Tag(name=name, user_id=user_id, order_in_user=count_tags(user_id)))
        session.commit()


def bind_tag_to_quote(tag_id, quote_id):
    with Session(engine) as session:
        session.add(QuoteTag(quote_id=quote_id, tag_id=tag_id))
        session.commit()


def get_user_by_id(user_id: int) -> User:
    with Session(engine) as session:
        return session.query(User).filter_by(id=user_id).one()


def get_quotes_by_tags(user_id: int, tags: list[str]) -> list[Union[None, Quote]]:
    quotes = get_user_quotes(user_id)
    if tags:
        return [quote for quote in quotes if sorted([tag.name for tag in quote.tag]) == sorted(tags)]
    else:
        return quotes


def get_user_quotes(user_id: int) -> list[Union[None, Quote]]:
    with Session(engine) as session:
        return [quote for quote in session.query(Quote).filter(Quote.user_id == user_id)]


def get_user_quotes_in_range(user_id: int, quote_range: range) -> list[Union[None, Quote]]:
    with Session(engine) as session:
        return [
            quote for quote in session.query(Quote).filter(
                Quote.user_id == user_id,
                Quote.order_in_user.in_(quote_range)
            )
        ]


def get_quote_by_order_in_user(order_in_user: int) -> Union[Quote, None]:
    with Session(engine) as session:
        return session.query(Quote).filter_by(order_in_user=order_in_user).one()


def get_user_tags(user_id: int) -> list[Union[None, Quote]]:
    with Session(engine) as session:
        return session.query(Tag).filter_by(user_id=user_id)


def get_user_tags_in_range(user_id: int, tag_range: range):
    with Session(engine) as session:
        return [
            tag for tag in session.query(Tag).filter(
                Tag.user_id == user_id,
                Tag.order_in_user.in_(tag_range)
            )
        ]


def update_quote(quote_id: int, **kwargs) -> None:
    with Session(engine) as session:
        session.query(Quote).filter_by(id=quote_id).update(kwargs)


def delete_quote(quote_id: int) -> None:
    delete(Quote, quote_id)


def delete_tag(tag_id: int) -> None:
    delete(Tag, tag_id)


def delete(table: Base, id: int) -> None:
    with Session(engine) as session:
        session.query(table).filter_by(id=id).delete()


def count_quote(user_id: int) -> int:
    return count(Quote, user_id)


def count_tags(user_id: int) -> int:
    return count(Tag, user_id)


def count(table: Base, user_id: int) -> int:
    with Session(engine) as session:
        return session.query(table).filter_by(user_id=user_id).count()
