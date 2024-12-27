from datetime import datetime

import pytest


@pytest.fixture
def two_flights_journey_combination():
    return [
            {
                "flight_number": "XX1234",
                "departure_city": "BUE",
                "arrival_city": "MDQ",
                "departure_datetime": datetime(2024, 9, 11, 10, 0),
                "arrival_datetime": datetime(2024, 9, 11, 13, 0)
            },
            {
                "flight_number": "XX2234",
                "departure_city": "MDQ",
                "arrival_city": "MAD",
                "departure_datetime": datetime(2024, 9, 11, 14, 0),
                "arrival_datetime": datetime(2024, 9, 11, 16, 0)
            }
        ]