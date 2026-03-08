import json

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import plotly.express as px
from app.database import get_db
from app import schemas, crud
from analysis import recommender

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/top-rated", response_model=List[schemas.TopRatedMovie])
def get_top_rated_movies(min_ratings: int = 50, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_top_rated_movies(db, min_ratings, limit)

@router.get("/top-rated/chart")
def get_top_rated_chart(min_ratings: int = 50, limit: int = 10, db: Session = Depends(get_db)):
    """Returns a Plotly JSON chart of top-rated movies."""
    data = crud.get_top_rated_movies(db, min_ratings, limit)
    df = pd.DataFrame(data)
    if df.empty:
        return JSONResponse(content={"error": "No data available"}, status_code=404)

    fig = px.bar(
        df,
        x="title",
        y="avg_rating",
        title="Top Rated Movies",
        color="avg_rating",
        hover_data=["num_ratings"],
        labels={"title": "Movie", "avg_rating": "Average Rating"},
    )
    fig.update_layout(xaxis_tickangle=-45)
    return JSONResponse(content=json.loads(fig.to_json()))

@router.get("/genres/avg-rating", response_model=List[schemas.GenreStats])
def get_genre_ratings(db: Session = Depends(get_db)):
    return crud.get_genre_stats(db)

@router.get("/genres/chart")
def get_genre_chart(db: Session = Depends(get_db)):
    """Returns a Plotly JSON chart of average rating per genre."""
    genre_data = crud.get_genre_stats(db)
    df = pd.DataFrame(genre_data)
    if df.empty:
        return JSONResponse(content={"error": "No data available"}, status_code=404)

    fig = px.bar(
        df,
        x="genres",
        y="mean",
        title="Average Rating per Genre",
        color="mean",
        hover_data=["count"],
        labels={"genres": "Genre", "mean": "Average Rating"},
    )
    return JSONResponse(content=json.loads(fig.to_json()))

@router.get("/{movie_id}/similar", response_model=List[schemas.SimilarMovie])
def get_similar(movie_id: int, top_k: int = 5):
    return recommender.get_similar_movies(movie_id, top_k)
