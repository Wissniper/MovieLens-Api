from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import schemas, crud

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}/ratings", response_model=List[schemas.UserRatingHistory])
def get_user_ratings_history(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_rating_history(db, user_id)
