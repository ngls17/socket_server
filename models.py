import datetime

from sqlalchemy import Table, Column, Integer, String, DateTime, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from __init__ import engine

Base = declarative_base()


class ReturnedString(Base):
    __tablename__ = 'returned_string'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(16))
    date_time = Column(DateTime)

    def __init__(self, text):
        self.text = text
        self.date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def __repr__(self):
        return "<ReturnedString('%s', '%s')>" % (self.text, self.date_time)

    @classmethod
    def add(cls, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()

    @classmethod
    def find_by_time(cls, start_time, end_time):
        return session.query(cls).filter(and_(cls.date_time >= start_time.strftime('%Y-%m-%d %H:%M:%S'),
                                              cls.date_time <= end_time.strftime('%Y-%m-%d %H:%M:%S'))).count()


class Statistics(Base):
    __tablename__ = 'statistics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    char = Column(String(1))
    count = Column(Integer)
    count_at_first_place = Column(Integer)

    def __init__(self, char, count, count_at_first_place):
        self.char = char
        self.count = count
        self.count_at_first_place = count_at_first_place

    def __repr__(self):
        return "<Statitics('%s', '%s', '%s')>" % (self.char, self.count, self.count_at_first_place)

    @classmethod
    def find(cls, char):
        return session.query(cls).filter_by(char=char).first()

    @classmethod
    def get_table(cls):
        return session.query(cls).order_by(cls.char).all()

    @classmethod
    def add(cls, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()

    @classmethod
    def update(cls, char, count_at_first_place):
        obj = session.query(cls).filter_by(char=char).first()
        obj.count += 1
        obj.count_at_first_place += count_at_first_place
        session.commit()


# Create tables
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
