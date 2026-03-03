from sqlalchemy import Column, Integer, String, Float, BigInteger
from sqlalchemy.ext.declarative import declarative_base

class Base(declarative_base()):
    pass

class Movie(Base):
    __tablename__ = "movies"
    movie_id = Column(Integer, primary_key=True)
    title = Column(String)
    genres = Column(String)  # Pipe-separated: "Action|Comedy"

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    movie_id = Column(Integer)
    rating = Column(Float)  # 0.5-5.0
    timestamp = Column(BigInteger)
