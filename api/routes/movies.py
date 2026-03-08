from fastapi import APIRouter
import pandas as pd
from typing import List
from app.database import engine
from app import schemas
from sqlalchemy import text
from analysis import recommender

import plotly.express as px

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/top-rated", response_model=List[schemas.TopRatedMovie])
def get_top_rated_movies(min_ratings: int = 50, limit: int = 10):
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
    # Rond de gemiddelde rating af op 2 decimalen
    df['avg_rating'] = df['avg_rating'].round(2)
    return df.to_dict(orient="records")

@router.get("/genres/avg-rating", response_model=List[schemas.GenreStats])
def get_genre_ratings():
    query = text("""
        SELECT r.rating, m.genres 
        FROM ratings r 
        JOIN movies m ON r.movie_id = m.movie_id
    """)
    df = pd.read_sql_query(query, engine)

    # Split en Explode de genres
    df["genres"] = df["genres"].str.split("|")
    exploded = df.explode("genres")

    # Filter 'no genres listed' eruit
    exploded = exploded[exploded["genres"] != "(no genres listed)"]

    # Groepeer op genre en bereken gemiddelde rating en aantal
    genre_stats = exploded.groupby("genres")["rating"].agg(["mean", "count"])
    genre_stats = genre_stats.round(2).sort_values("mean", ascending=False)
    
    # Maak van de index weer een gewone kolom en zet om naar dict list
    return genre_stats.reset_index().to_dict(orient="records")

@router.get("/genres/chart")
def get_genre_chart():
    # Zelfde logica als hierboven, maar dan voor een visualisatie
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
    genre_stats = genre_stats.round(2).reset_index()

    fig = px.bar(
        genre_stats, 
        x="genres", 
        y="mean", 
        title="Gemiddelde Rating per Genre",
        color="mean",
        hover_data=["count"]
    )
    
    return fig.to_json()

@router.get("/{movie_id}/similar", response_model=List[schemas.SimilarMovie])
def get_similar(movie_id: int, top_k: int = 5):
    return recommender.get_similar_movies(movie_id, top_k)
