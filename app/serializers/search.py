import datetime
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator, ValidationError
from starlette import status


class JourneySearchParams(BaseModel):
    departure: str = Field(max_length=3, min_length=3)
    destination: str = Field(max_length=3, min_length=3)
    date: datetime.date

    @field_validator("date")
    def validate_date_is_not_in_the_past(cls, date):
        if date < datetime.date.today():
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Date cannot be in the past")
        return date

class Trip(BaseModel):
    arrival_time: datetime.datetime
    departure_time:  datetime.datetime
    trip_number: str
    from_: str
    to: str

class JourneySearchResponse(BaseModel):
    connections: int
    path: List[Trip]