from pydantic import BaseModel
from typing import List, Optional

class TopRatedMovie(BaseModel):
    movie_id: int
    title: str
    genres: str
    avg_rating: float
    num_ratings: int
    rank: int

class GenreStats(BaseModel):
    genres: str
    mean: float
    count: int

class UserRatingHistory(BaseModel):
    title: str
    rating: float
    moving_avg: Optional[float]
    date: str

class SimilarMovie(BaseModel):
    movie_id: int
    title: str
    genres: str
    similarity_score: float

class OverallStats(BaseModel):
    total_movies: int
    total_ratings: int
    unique_users: int
    average_rating: float

class RatingDistribution(BaseModel):
    rating: float
    count: int