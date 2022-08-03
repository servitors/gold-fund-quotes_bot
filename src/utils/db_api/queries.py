import typing

from sqlalchemy.dialects import postgresql
from sqlalchemy import orm

from utils.db_api import schemas
from utils.db_api import base


def add_user_in_db(session: orm.Session, telegram_id: int, name: str) -> None:
    statement = postgresql.insert(schemas.User).values(id=telegram_id, name=name)
    statement = statement.on_conflict_do_nothing(index_elements=[schemas.User.id])
    session.execute(statement)


def add_quote_in_db(session: orm.Session, user_id: int, **kwargs) -> None:
    session.add(schemas.Quote(user_id=user_id, order_in_user=count_quote(user_id), **kwargs))


def add_tag_in_db(session: orm.Session, name: str, user_id: int) -> None:
    session.add(schemas.Tag(name=name, user_id=user_id, order_in_user=count_tags(user_id)))


def bind_tag_to_quote(session: orm.Session, tag_id, quote_id):
    session.add(schemas.QuoteTag(quote_id=quote_id, tag_id=tag_id))


def get_user_by_id(session: orm.Session, user_id: int) -> schemas.User:
    return session.query(schemas.User).filter_by(id=user_id).one()


def get_quotes_by_tags(user_id: int, tags: list[str]) -> list[schemas.Quote | None]:
    quotes = get_user_quotes(user_id)
    if tags:
        return [quote for quote in quotes if sorted([tag.name for tag in quote.tag]) == sorted(tags)]
    else:
        return quotes


def get_user_quotes(session: orm.Session, user_id: int) -> list[schemas.Quote | None]:
    return [quote for quote in session.query(schemas.Quote).filter(schemas.Quote.user_id == user_id)]


def get_user_quotes_in_range(session: orm.Session, user_id: int, quote_range: range) -> list[schemas.Quote | None]:
    return [
        quote for quote in session.query(schemas.Quote).filter(
            schemas.Quote.user_id == user_id,
            schemas.Quote.order_in_user.in_(quote_range)
        )
    ]


def get_quote_by_order_in_user(session: orm.Session, order_in_user: int) -> schemas.Quote | None:
    return session.query(schemas.Quote).filter_by(order_in_user=order_in_user).one()


def get_user_tags(session: orm.Session, user_id: int) -> list[schemas.Quote | None]:
    return session.query(schemas.Tag).filter_by(user_id=user_id)


def get_user_tags_in_range(session: orm.Session, user_id: int, tag_range: range):
    return [
        tag for tag in session.query(schemas.Tag).filter(
            schemas.Tag.user_id == user_id,
            schemas.Tag.order_in_user.in_(tag_range)
        )
    ]


def update_quote(session: orm.Session, quote_id: int, **kwargs) -> None:
    session.query(schemas.Quote).filter_by(id=quote_id).update(kwargs)


def delete_quote(session: orm.Session, quote_id: int) -> None:
    session.query(schemas.Quote).filter_by(id=quote_id).delete()


def delete_tag(session: orm.Session, tag_id: int) -> None:
    session.query(schemas.Tag).filter_by(id=tag_id).delete()


def count_user_quotes(session: orm.Session, user_id: int) -> int:
    return session.query(schemas.Quote).filter_by(user_id=user_id).count()


def count_user_tags(session: orm.Session, user_id: int) -> int:
    return session.query(schemas.Tag).filter_by(user_id=user_id).count()
