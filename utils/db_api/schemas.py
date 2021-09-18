from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from utils.db_api.base import Base


class User(Base):

    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(255))
    quote = relationship('Quote', backref="users")
    tags = relationship('Tag', backref='users')


class Quote(Base):

    __tablename__ = 'quote'
    id = Column('id', Integer, primary_key=True)
    content = Column('content', Text)
    author = Column('author', String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    tags = relationship('Tag', secondary='quote_tag', backref='quote')


class Tag(Base):

    __tablename__ = 'tag'
    id = Column('id', Integer, primary_key=True)
    tag = Column('tag', String(30))
    user_id = Column(Integer, ForeignKey('users.id'))


class QuoteTag(Base):
    __tablename__ = 'quote_tag'

    quote_id = Column(Integer, ForeignKey('quote.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tag.id'), primary_key=True)
