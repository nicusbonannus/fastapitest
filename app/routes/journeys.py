from typing import List

import joblib
import pandas as pd
from fastapi import APIRouter, Depends

from app.domain.trip_search_engine import TripSearchEngine, JourneyPlan
from app.serializers.search import JourneySearchParams, JourneySearchResponse

router = APIRouter()


@router.get("/search", response_model=List[JourneySearchResponse])
async def get_search(params: JourneySearchParams = Depends()):
    return TripSearchEngine().search(params.departure, params.destination, params.date)


@router.post("/calculate")
async def calculate_journey():
    plan = JourneyPlan(Duration=0.549637, Total_Stops=2, Source=2, Destination=1, Additional_Info=8, Dep_Time=0.385159,
                       Arrival_Time=0.181818, Day=9, Month=6, Year=2024)
    price = TripSearchEngine().calculate_price(plan)
    return {"prediction": price}
