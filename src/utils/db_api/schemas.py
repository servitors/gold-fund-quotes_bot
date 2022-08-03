from sqlalchemy import orm, sql
import sqlalchemy

from utils.db_api import base


__all__ = ('User', 'Quote', 'Tag', 'QuoteTag')


class BaseModel(base.Base):
    __abstract__ = True

    id = sqlalchemy.Column(
        sqlalchemy.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True
    )
    created_at = sqlalchemy.Column(sqlalchemy.TIMESTAMP, server_default=sql.func.now())
    updated_at = sqlalchemy.Column(sqlalchemy.TIMESTAMP, onupdate=sql.func.current_timestamp())

    def __repr__(self):
        return f"{type(self).__name__}(id={self.id})"


class User(base.Base):

    __tablename__ = 'users'

    name = sqlalchemy.Column(sqlalchemy.String(255))
    quote = orm.relationship('Quote', backref="users")
    tag = orm.relationship('Tag', backref='users')


class Quote(base.Base):

    __tablename__ = 'quote'

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    content = sqlalchemy.Column(sqlalchemy.Text)
    author = sqlalchemy.Column(sqlalchemy.String(255))
    order_in_user = sqlalchemy.Column(sqlalchemy.Integer)
    tag = orm.relationship('Tag', lazy='subquery', secondary='quote_tag', backref='quote')


class Tag(base.Base):

    __tablename__ = 'tag'
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    name = sqlalchemy.Column(sqlalchemy.String(32))
    order_in_user = sqlalchemy.Column(sqlalchemy.Integer)


class QuoteTag(base.Base):
    __tablename__ = 'quote_tag'

    quote_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('quote.id'), primary_key=True)
    tag_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tag.id'), primary_key=True)
