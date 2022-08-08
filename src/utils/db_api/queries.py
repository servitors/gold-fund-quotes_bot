from sqlalchemy import orm
import sqlalchemy.exc
import sqlalchemy

from utils.db_api import schemas


def add_user_to_db(session: orm.Session, telegram_id: int, name: str) -> schemas.User:
    user = schemas.User(telegram_id=telegram_id, name=name)
    session.add(user)
    session.flush()
    session.expire(user)
    return user


def add_quote_to_db(session: orm.Session, user_id: int, **kwargs) -> schemas.Quote:
    quote = schemas.Quote(user_id=user_id, **kwargs)
    session.add(quote)
    session.flush()
    session.expire(quote)
    return quote


def add_tag_to_db(session: orm.Session, name: str, user_id: int) -> schemas.Tag:
    tag = schemas.Tag(name=name, user_id=user_id)
    session.add(tag)
    session.flush()
    session.expire(tag)
    return tag


def add_tags_to_db(session: orm.Session, names: list[str], user_id: int) -> list[schemas.Tag]:
    tags = [schemas.Tag(name=name, user_id=user_id) for name in names]
    session.add_all(tags)
    session.flush()
    session.expire_all()
    return tags


def bind_tag_to_quote(session: orm.Session, tag_id: int, quote_id: int):
    session.add(schemas.QuoteTag(quote_id=quote_id, tag_id=tag_id))


def get_user_by_id(session: orm.Session, user_id: int) -> schemas.User | None:
    user = session.get(schemas.User, user_id)
    session.expunge(user)
    return user


def get_quotes_by_tags(session: orm.Session, user_id: int, tags: list[str]) -> list[schemas.Quote | None]:
    ...


def get_user_quotes(
        session: orm.Session, user_id: int,
        page: int = None, page_size: int = None) -> list[schemas.Quote | None]:

    statement = sqlalchemy.select(schemas.Quote).filter_by(user_id=user_id)
    statement = statement.order_by('created_at')
    if page and page_size:
        statement = statement.limit(page_size).offset(page * page_size)

    quotes = session.scalars(statement).all()
    session.expunge_all()
    return quotes


def get_user_tags(session: orm.Session, user_id: int,
                  page: int = None, page_size: int = None) -> list[schemas.Tag | None]:
    statement = sqlalchemy.select(schemas.Tag).filter_by(user_id=user_id).order_by('created_at')
    if page and page_size:
        statement = statement.limit(page_size).offset(page * page_size)
    tags = session.scalars(statement).all()
    session.expire_all()
    return tags


def get_user_quote(session: orm.Session, quote_id: int, user_id) -> schemas.Quote | None:
    statement = sqlalchemy.select(schemas.Quote).filter_by(id=quote_id, user_id=user_id)
    quote = session.scalars(statement).first()
    session.expunge(quote)
    return quote


def update_quote(session: orm.Session, quote_id: int, **kwargs) -> None:
    session.execute(
        sqlalchemy.update(schemas.Quote).
        where(schemas.Quote.id == quote_id).
        values(**kwargs)
    )


def delete_quote(session: orm.Session, quote_id: int) -> None:
    session.execute(
        sqlalchemy.delete(schemas.Tag).where(schemas.Quote.id == quote_id)
    )


def delete_tag(session: orm.Session, tag_id: int) -> None:
    session.execute(
        sqlalchemy.delete(schemas.Tag).where(schemas.Tag.id == tag_id)
    )


def count_user_quotes(session: orm.Session, user_id: int) -> int:
    statement = sqlalchemy.select(
        sqlalchemy.func.count(schemas.Quote.id)
    ).filter_by(user_id=user_id)
    return session.scalar(statement)


def count_user_tags(session: orm.Session, user_id: int) -> int:
    statement = sqlalchemy.select(
        sqlalchemy.func.count(schemas.Tag.id)
    ).filter_by(user_id=user_id)
    return session.scalar(statement)
