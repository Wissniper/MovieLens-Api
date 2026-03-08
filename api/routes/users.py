from fastapi import APIRouter
import pandas as pd
from typing import List
from sqlalchemy import text
from app.database import engine
from app import schemas

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}/ratings", response_model=List[schemas.UserRatingHistory])
def get_user_ratings_history(user_id: int):
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
    
    # Als de gebruiker geen beoordelingen heeft, geef een lege lijst terug
    if df.empty:
        return []
    
    # Tijdstempel omzetten naar leesbare datum
    df["date"] = pd.to_datetime(df["timestamp"], unit="s").dt.strftime("%Y-%m-%d")
    df = df.drop(columns=["timestamp"])
    
    # Waardes afronden op 2 decimalen
    df["moving_avg"] = df["moving_avg"].round(2)
    
    return df.to_dict(orient="records")
