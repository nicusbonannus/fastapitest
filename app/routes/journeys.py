from typing import List

from fastapi import APIRouter, Depends

from app.domain.flight_search_engine import FlightSearchEngine
from app.serializers.search import JourneySearchParams, JourneySearchResponse

router = APIRouter()

@router.get("/search", response_model=List[JourneySearchResponse])
async def get_search(params: JourneySearchParams=Depends()):
    return FlightSearchEngine().search(params.departure, params.destination, params.date)


