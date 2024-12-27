from fastapi import APIRouter, Depends

from app.domain.flight_search_engine import FlightSearchEngine
from app.serializers.journey_search_parameters import JourneySearchParams

router = APIRouter()

@router.get("/search")
# TODO: Create serializer for response
async def get_search(params: JourneySearchParams= Depends()):
    return FlightSearchEngine().search(params.departure, params.destination, params.date)


