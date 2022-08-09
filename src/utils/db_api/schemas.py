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


class User(BaseModel):

    __tablename__ = 'users'

    telegram_id = sqlalchemy.Column(sqlalchemy.BigInteger, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String(255))
    quotes = orm.relationship('Quote', backref="users")
    tags = orm.relationship('Tag', backref='users')


class Quote(BaseModel):

    __tablename__ = 'quote'

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    content = sqlalchemy.Column(sqlalchemy.Text)
    author = sqlalchemy.Column(sqlalchemy.String(255))
    tags = orm.relationship('QuoteTag', back_populates='quote')


class Tag(BaseModel):

    __tablename__ = 'tag'
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    name = sqlalchemy.Column(sqlalchemy.String(32))
    quotes = orm.relationship('QuoteTag', back_populates='tag')


class QuoteTag(BaseModel):
    __tablename__ = 'quote_tag'

    quote_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('quote.id'), primary_key=True)
    tag_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tag.id'), primary_key=True)
    quote = orm.relationship('Quote', back_populates='tags')
    tag = orm.relationship('Tag', back_populates='quotes')
