from fastapi import APIRouter
from typing import List
from app import schemas
from analysis.stats import get_overall_stats, get_rating_distribution

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/overview", response_model=schemas.OverallStats)
def overview():
    return get_overall_stats()

@router.get("/rating-distribution", response_model=List[schemas.RatingDistribution])
def rating_distribution():
    return get_rating_distribution()
