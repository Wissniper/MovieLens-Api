from fastapi import APIRouter
import pandas as pd
from app.database import engine
from sqlalchemy import text

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/top-rated")
def get_top_rated_movies(min_ratings: int = 50):
    query = text("""
        SELECT m.movie_id, m.title, m.genres, AVG(r.rating) as avg_rating, COUNT(r.rating) as num_ratings,
        ROW_NUMBER() OVER (ORDER BY avg_rating DESC) as rank
        FROM movies m
        JOIN ratings r ON m.movie_id = r.movie_id
        GROUP BY m.movie_id, m.title, m.genres
        HAVING COUNT(r.rating) >= :min_ratings
        ORDER BY avg_rating DESC
        LIMIT 10
    """)
    df = pd.read_sql_query(query, engine, params={"min_ratings": min_ratings})
    return df.to_dict(orient="records") # Convert DataFrame to list of dicts for JSON response