import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import engine

def get_top_rated_movies(db: Session, min_ratings: int = 50, limit: int = 10):
    query = text("""
        SELECT m.movie_id, m.title, m.genres, 
               AVG(r.rating) as avg_rating, 
               COUNT(r.rating) as num_ratings,
               ROW_NUMBER() OVER (ORDER BY AVG(r.rating) DESC) as rank
        FROM movies m
        JOIN ratings r ON m.movie_id = r.movie_id
        GROUP BY m.movie_id, m.title, m.genres
        HAVING COUNT(r.rating) >= :min_ratings
        ORDER BY avg_rating DESC
        LIMIT :limit
    """)
    df = pd.read_sql_query(query, engine, params={"min_ratings": min_ratings, "limit": limit})
    df['avg_rating'] = df['avg_rating'].round(2)
    return df.to_dict(orient="records")

def get_genre_stats(db: Session):
    query = text("""
        SELECT r.rating, m.genres 
        FROM ratings r 
        JOIN movies m ON r.movie_id = m.movie_id
    """)
    df = pd.read_sql_query(query, engine)
    df["genres"] = df["genres"].str.split("|")
    exploded = df.explode("genres")
    exploded = exploded[exploded["genres"] != "(no genres listed)"]
    
    genre_stats = exploded.groupby("genres")["rating"].agg(["mean", "count"])
    genre_stats = genre_stats.round(2).sort_values("mean", ascending=False)
    return genre_stats.reset_index().to_dict(orient="records")

def get_user_rating_history(db: Session, user_id: int):
    query = text("""
        SELECT m.title, r.rating, r.timestamp,
               AVG(r.rating) OVER (
                   ORDER BY r.timestamp 
                   ROWS BETWEEN 10 PRECEDING AND CURRENT ROW
               ) as moving_avg
        FROM ratings r 
        JOIN movies m ON r.movie_id = m.movie_id
        WHERE r.user_id = :user_id 
        ORDER BY r.timestamp;
    """)
    df = pd.read_sql_query(query, engine, params={"user_id": user_id})
    if df.empty:
        return []
    
    df["date"] = pd.to_datetime(df["timestamp"], unit="s").dt.strftime("%Y-%m-%d")
    df = df.drop(columns=["timestamp"]).round(2)
    return df.to_dict(orient="records")
