from datetime import datetime

import pytest


@pytest.fixture
def two_trips_journey_combination():
    return [
        {
            "trip_number": "XX1234",
            "departure_city": "BUE",
            "arrival_city": "MDQ",
            "departure_datetime": datetime(2024, 9, 11, 10, 0),
            "arrival_datetime": datetime(2024, 9, 11, 13, 0)
        },
        {
            "trip_number": "XX2234",
            "departure_city": "MDQ",
            "arrival_city": "MAD",
            "departure_datetime": datetime(2024, 9, 11, 14, 0),
            "arrival_datetime": datetime(2024, 9, 11, 16, 0)
        }
    ]


@pytest.fixture
def one_trip_journey_combination():
    return [
        {
            "trip_number": "XX1234",
            "departure_city": "BUE",
            "arrival_city": "MAD",
            "departure_datetime": datetime(2024, 9, 11, 10, 0),
            "arrival_datetime": datetime(2024, 9, 11, 23, 0)
        }
    ]


@pytest.fixture
def one_trip_journey_combination_with_another_destiny():
    return [
        {
            "trip_number": "XX1234",
            "departure_city": "BUE",
            "arrival_city": "POR",
            "departure_datetime": datetime(2024, 9, 11, 10, 0),
            "arrival_datetime": datetime(2024, 9, 11, 23, 0)
        }
    ]


@pytest.fixture
def one_trip_journey_combination_with_another_origin():
    return [
        {
            "trip_number": "XX1234",
            "departure_city": "MDQ",
            "arrival_city": "POR",
            "departure_datetime": datetime(2024, 9, 11, 10, 0),
            "arrival_datetime": datetime(2024, 9, 11, 23, 0)
        }
    ]

@pytest.fixture
def one_trip_journey_combination_of_two_trips_with_another_destiny():
    return [
        {
            "trip_number": "XX1234",
            "departure_city": "BUE",
            "arrival_city": "POR",
            "departure_datetime": datetime(2024, 9, 11, 10, 0),
            "arrival_datetime": datetime(2024, 9, 11, 23, 0)
        },

        {
            "trip_number": "XX1234",
            "departure_city": "POR",
            "arrival_city": "MDQ",
            "departure_datetime": datetime(2024, 9, 11, 10, 0),
            "arrival_datetime": datetime(2024, 9, 11, 23, 0)
        }
    ]

@pytest.fixture
def one_trip_for_total_more_than_24_hours():
    return [
        {
            "trip_number": "XX1234",
            "departure_city": "BUE",
            "arrival_city": "MAD",
            "departure_datetime": datetime(2024, 9, 11, 10, 0),
            "arrival_datetime": datetime(2024, 9, 12, 10, 1)
        },
    ]


@pytest.fixture
def two_trips_for_total_more_than_24_hours():
    return [
        {
            "trip_number": "XX1234",
            "departure_city": "BUE",
            "arrival_city": "MDQ",
            "departure_datetime": datetime(2024, 9, 11, 10, 0),
            "arrival_datetime": datetime(2024, 9, 11, 13, 0)
        },
        {
            "trip_number": "XX2234",
            "departure_city": "MDQ",
            "arrival_city": "MAD",
            "departure_datetime": datetime(2024, 9, 11, 14, 0),
            "arrival_datetime": datetime(2024, 9, 12, 10, 1)
        }
    ]


@pytest.fixture
def trips_with_a_big_connection():
    return [
        {
            "trip_number": "XX1234",
            "departure_city": "BUE",
            "arrival_city": "MDQ",
            "departure_datetime": datetime(2024, 9, 11, 10, 0),
            "arrival_datetime": datetime(2024, 9, 11, 13, 0)
        },
        {
            "trip_number": "XX2234",
            "departure_city": "MDQ",
            "arrival_city": "MAD",
            "departure_datetime": datetime(2024, 9, 11, 17, 1),
            "arrival_datetime": datetime(2024, 9, 12, 6, 0)
        }
    ]


@pytest.fixture
def multiple_trip_combinations():
    return [
        {
            "trip_number": "XX1234",
            "departure_city": "BUE",
            "arrival_city": "MDQ",
            "departure_datetime": datetime(2024, 9, 11, 10, 0),
            "arrival_datetime": datetime(2024, 9, 11, 13, 0)
        },
        {
            "trip_number": "XX2234",
            "departure_city": "MDQ",
            "arrival_city": "MAD",
            "departure_datetime": datetime(2024, 9, 11, 14, 0),
            "arrival_datetime": datetime(2024, 9, 11, 16, 0)
        },
        {
            "trip_number": "XX3234",
            "departure_city": "MDQ",
            "arrival_city": "MAD",
            "departure_datetime": datetime(2024, 9, 11, 15, 0),
            "arrival_datetime": datetime(2024, 9, 11, 17, 0)
        }
    ]
