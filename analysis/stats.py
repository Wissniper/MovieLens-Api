import pandas as pd
from sqlalchemy import text
from app.database import engine

def get_overall_stats():
    """
    Returns high-level statistics of the dataset.
    """
    with engine.connect() as conn:
        movie_count = conn.execute(text("SELECT COUNT(*) FROM movies")).scalar()
        rating_count = conn.execute(text("SELECT COUNT(*) FROM ratings")).scalar()
        user_count = conn.execute(text("SELECT COUNT(DISTINCT user_id) FROM ratings")).scalar()
        avg_rating = conn.execute(text("SELECT AVG(rating) FROM ratings")).scalar()
        
    return {
        "total_movies": movie_count,
        "total_ratings": rating_count,
        "unique_users": user_count,
        "average_rating": round(avg_rating, 2)
    }

def get_rating_distribution():
    """
    Returns the distribution of ratings.
    """
    query = text("SELECT rating, COUNT(*) as count FROM ratings GROUP BY rating ORDER BY rating")
    df = pd.read_sql_query(query, engine)
    return df.to_dict(orient="records")
