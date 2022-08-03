import typing

from sqlalchemy.dialects import postgresql
from sqlalchemy import orm
import sqlalchemy.exc

from utils.db_api import schemas
from utils.db_api import engine, base


def add_user_in_db(id: int, name: str) -> bool:
    statement = postgresql.insert(schemas.User).values(id=id, name=name)
    statement = statement.on_conflict_do_nothing(index_elements=[schemas.User.id])
    with orm.Session(engine) as session:
        try:
            session.execute(statement)
        except sqlalchemy.exc.IntegrityError:
            return False
        else:
            session.commit()
            return True


def add_quote_in_db(user_id: int, **kwargs) -> None:
    with orm.Session(engine) as session:
        session.add(schemas.Quote(user_id=user_id, order_in_user=count_quote(user_id), **kwargs))
        session.commit()


def add_tag_in_db(name: str, user_id: int) -> None:
    with orm.Session(engine) as session:
        session.add(schemas.Tag(name=name, user_id=user_id, order_in_user=count_tags(user_id)))
        session.commit()


def bind_tag_to_quote(tag_id, quote_id):
    with orm.Session(engine) as session:
        session.add(schemas.QuoteTag(quote_id=quote_id, tag_id=tag_id))
        session.commit()


def get_user_by_id(user_id: int) -> schemas.User:
    with orm.Session(engine) as session:
        return session.query(schemas.User).filter_by(id=user_id).one()


def get_quotes_by_tags(user_id: int, tags: list[str]) -> list[typing.Union[None, schemas.Quote]]:
    quotes = get_user_quotes(user_id)
    if tags:
        return [quote for quote in quotes if sorted([tag.name for tag in quote.tag]) == sorted(tags)]
    else:
        return quotes


def get_user_quotes(user_id: int) -> list[typing.Union[None, schemas.Quote]]:
    with orm.Session(engine) as session:
        return [quote for quote in session.query(schemas.Quote).filter(schemas.Quote.user_id == user_id)]


def get_user_quotes_in_range(user_id: int, quote_range: range) -> list[typing.Union[None, schemas.Quote]]:
    with orm.Session(engine) as session:
        return [
            quote for quote in session.query(schemas.Quote).filter(
                schemas.Quote.user_id == user_id,
                schemas.Quote.order_in_user.in_(quote_range)
            )
        ]


def get_quote_by_order_in_user(order_in_user: int) -> typing.Union[schemas.Quote, None]:
    with orm.Session(engine) as session:
        return session.query(schemas.Quote).filter_by(order_in_user=order_in_user).one()


def get_user_tags(user_id: int) -> list[typing.Union[None, schemas.Quote]]:
    with orm.Session(engine) as session:
        return session.query(schemas.Tag).filter_by(user_id=user_id)


def get_user_tags_in_range(user_id: int, tag_range: range):
    with orm.Session(engine) as session:
        return [
            tag for tag in session.query(schemas.Tag).filter(
                schemas.Tag.user_id == user_id,
                schemas.Tag.order_in_user.in_(tag_range)
            )
        ]


def update_quote(quote_id: int, **kwargs) -> None:
    with orm.Session(engine) as session:
        session.query(schemas.Quote).filter_by(id=quote_id).update(kwargs)


def delete_quote(quote_id: int) -> None:
    delete(schemas.Quote, quote_id)


def delete_tag(tag_id: int) -> None:
    delete(schemas.Tag, tag_id)


def delete(table: base.Base, id: int) -> None:
    with orm.Session(engine) as session:
        session.query(table).filter_by(id=id).delete()


def count_quote(user_id: int) -> int:
    return count(schemas.Quote, user_id)


def count_tags(user_id: int) -> int:
    return count(schemas.Tag, user_id)


def count(table: base.Base, user_id: int) -> int:
    with orm.Session(engine) as session:
        return session.query(table).filter_by(user_id=user_id).count()
