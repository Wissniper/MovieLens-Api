from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import plotly.express as px
from app.database import engine, get_db
from app import schemas, crud
from analysis import recommender

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/top-rated", response_model=List[schemas.TopRatedMovie])
def get_top_rated_movies(min_ratings: int = 50, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_top_rated_movies(db, min_ratings, limit)

@router.get("/genres/avg-rating", response_model=List[schemas.GenreStats])
def get_genre_ratings(db: Session = Depends(get_db)):
    return crud.get_genre_stats(db)

@router.get("/genres/chart")
def get_genre_chart(db: Session = Depends(get_db)):
    genre_data = crud.get_genre_stats(db)
    df = pd.DataFrame(genre_data)

    fig = px.bar(
        df, 
        x="genres", 
        y="mean", 
        title="Gemiddelde Rating per Genre",
        color="mean",
        hover_data=["count"]
    )
    
    return fig.to_json()

@router.get("/{movie_id}/similar", response_model=List[schemas.SimilarMovie])
def get_similar(movie_id: int, top_k: int = 5):
    # De recommender gebruikt direct de engine, we laten dit nu zo.
    return recommender.get_similar_movies(movie_id, top_k)
