from typing import List

from fastapi import APIRouter, Depends

from app.domain.trip_search_engine import TripSearchEngine
from app.serializers.search import JourneySearchParams, JourneySearchResponse

router = APIRouter()

@router.get("/search", response_model=List[JourneySearchResponse])
async def get_search(params: JourneySearchParams=Depends()):
    return TripSearchEngine().search(params.departure, params.destination, params.date)


