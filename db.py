from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///blog.sqlite')

db_session = scoped_session(sessionmaker(bind=engine))


Base = declarative_base()
Base.query = db_session.query_property()


class User(Base):
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

    def __init__(self, first_name=None, last_name=None, email=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        return '<User {} {}>'.format(self.first_name, self.last_name)


class Cafe(Base):
    """Table with coffee shops"""
    __tablename__ = 'coffee_shops'


    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    address = Column(String(150))
    average_receipt = Column(Integer)
    # geo_location = Column() ??


    def __init__(self, name=None, address=None, average_receipt=None):
        self.name = name
        self.address = address
        self.average_receipt = average_receipt

    def __repr__(self):
        return 'Cafe {}'.format(self.name)

class Tag(Base):
    """Table with tags characterizing cafe"""
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tag_name = Column(String(120))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "Tag {}".format(self.name)


class Tags_for_cafe(Base):
    """Table for an associate of cafes and tags for it"""

    tag_id = Column(Integer, ForeignKey('tags.id'))
    cafe_id = Column(Integer, ForeignKey('coffee_shops.id'))

    def __init__(self, tag_id=None, cafe_id=None):
        self.tag_id = tag_id
        self.cafe_id = cafe_id 
    
    def __repr__(self):
        return "{} is associated with {}".format(cafe_id, tag_id)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)