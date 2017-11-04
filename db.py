from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, SmallInteger, Float
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from hashlib import md5
from flask_login import UserMixin

engine = create_engine('sqlite:///db.sqlite')
db_session = scoped_session(sessionmaker(bind=engine))


Base = declarative_base()
Base.query = db_session.query_property()


class User(Base, UserMixin):
    """Table with registered users"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String(50))
    password = Column(String(50))
    address = Column(String(120))
    favorite_cafe = Column(Integer, ForeignKey('coffee_shops.id'))
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(120), unique = True)

    def __repr__(self):
        return '<User {} {} {}>'.format(self.first_name, self.last_name, self.email)

    def __init__(self, email='', password='', first_name='', last_name=''):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def avatar(self, size):
        return 'https://robohash.org/{}?set=set3'.format(self.last_name)


class Cafe(Base):
    """Table with coffee shops"""
    __tablename__ = 'coffee_shops'


    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    address = Column(String(150))
    average_receipt = Column(Integer)
    image_url = Column(String(200))
    lat = Column(Float)
    lng = Column(Float)
    rating = Column(SmallInteger)


    def __repr__(self):
        return 'Cafe {}'.format(self.name)

class Tag(Base):
    """Table with tags characterizing cafe"""
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tag_name = Column(String(120))
    localized_name = Column(String(120))


    def __repr__(self):
        return "Tag {}".format(self.name)


class TagsForCafe(Base):
    """Table for an associate of cafes and tags for it"""
    __tablename__ = 'tags_for_cafe'

    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'))
    cafe_id = Column(Integer, ForeignKey('coffee_shops.id'))

    
    def __repr__(self):
        return "{} is associated with {}".format(cafe_id, tag_id)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)