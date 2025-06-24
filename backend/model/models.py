from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from model.database import Base

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    release_date = Column(String)
    director = Column(String, nullable=False)
    category = Column(String, nullable=False)
    poster_url = Column(String, nullable=True)
    
    reviews = relationship("Review", back_populates="movie", cascade="all, delete")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    author = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    sentiment = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    
    movie = relationship("Movie", back_populates="reviews")