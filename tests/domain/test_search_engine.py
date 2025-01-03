from datetime import datetime
from unittest.mock import patch, ANY

from freezegun import freeze_time

from app.domain.trip_search_engine import TripSearchEngine
from tests.fixtures import *


@freeze_time("2024-09-11")
class TestSearchEngine:
    # NOTE: I haven't tested the case of journeys from another date since I assume we can filter
    # the journeys by date from the API
    @patch("app.domain.trips_api.TripsAPI.get_trips")
    def test_search_journeys_happy_path(self, mock_get_trips, one_trip_journey_combination):
        # given
        mock_get_trips.return_value = one_trip_journey_combination
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = TripSearchEngine().search(departure, destination, date)

        # then
        assert result == [{"connections": 1, "path": [{"trip_number": "XX1234", "from_": "BUE", "to": "MAD",
                                                       "departure_time": ANY,
                                                       "arrival_time": ANY}]}]

    @patch("app.domain.trips_api.TripsAPI.get_trips")
    def test_search_journeys_with_combinations(self, mock_get_trips, two_trips_journey_combination):
        # given
        mock_get_trips.return_value = two_trips_journey_combination
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = TripSearchEngine().search(departure, destination, date)

        # then
        assert result == [{"connections": 2,
                           "path": [
                               {"trip_number": "XX1234",
                                "from_": "BUE",
                                "to": "MDQ",
                                "departure_time": ANY,
                                "arrival_time": ANY},
                               {"trip_number": "XX2234",
                                "from_": "MDQ",
                                "to": "MAD",
                                "departure_time": ANY,
                                "arrival_time": ANY},
                           ]}]

    @patch("app.domain.trips_api.TripsAPI.get_trips")
    def test_search_journeys_one_destination_that_does_not_match(self, mock_get_trips,
                                                                 one_trip_journey_combination_with_another_destiny):
        # given
        mock_get_trips.return_value = one_trip_journey_combination_with_another_destiny
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = TripSearchEngine().search(departure, destination, date)

        # then
        assert result == []

    @patch("app.domain.trips_api.TripsAPI.get_trips")
    def test_search_journeys_one_origin_that_does_not_match(self, mock_get_trips,
                                                            one_trip_journey_combination_of_two_trips_with_another_destiny):
        # given
        mock_get_trips.return_value = one_trip_journey_combination_of_two_trips_with_another_destiny
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = TripSearchEngine().search(departure, destination, date)

        # then
        assert result == []

    @patch("app.domain.trips_api.TripsAPI.get_trips")
    def test_search_journeys_two_combinations_available(self, mock_get_trips, multiple_trip_combinations):
        # given
        mock_get_trips.return_value = multiple_trip_combinations
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = TripSearchEngine().search(departure, destination, date)

        # then
        assert result == [{"connections": 2,
                           "path": [
                               {"trip_number": "XX1234",
                                "from_": "BUE",
                                "to": "MDQ",
                                "departure_time": ANY,
                                "arrival_time": ANY},
                               {"trip_number": "XX2234",
                                "from_": "MDQ",
                                "to": "MAD",
                                "departure_time": ANY,
                                "arrival_time": ANY},
                           ]},
                          {"connections": 2,
                           "path": [
                               {"trip_number": "XX1234",
                                "from_": "BUE",
                                "to": "MDQ",
                                "departure_time": ANY,
                                "arrival_time": ANY},
                               {"trip_number": "XX3234",
                                "from_": "MDQ",
                                "to": "MAD",
                                "departure_time": ANY,
                                "arrival_time": ANY},
                           ]}
                          ]

    @patch("app.domain.trips_api.TripsAPI.get_trips")
    def test_search_journeys_only_one_journey_of_more_than_24_hs_available(self, mock_get_trips,
                                                                           one_trip_for_total_more_than_24_hours):
        # given
        mock_get_trips.return_value = one_trip_for_total_more_than_24_hours
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = TripSearchEngine().search(departure, destination, date)

        # then
        assert result == []

    @patch("app.domain.trips_api.TripsAPI.get_trips")
    def test_search_journeys_one_combinations_for_more_than_24_hs_available(self, mock_get_trips,
                                                                            two_trips_for_total_more_than_24_hours):
        # given
        mock_get_trips.return_value = two_trips_for_total_more_than_24_hours
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = TripSearchEngine().search(departure, destination, date)

        # then
        assert result == []

    @patch("app.domain.trips_api.TripsAPI.get_trips")
    def test_search_journeys_one_combination_with_a_connection_of_more_than_4_hs_available(self, mock_get_trips,
                                                                                           trips_with_a_big_connection):
        # given
        mock_get_trips.return_value = trips_with_a_big_connection
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = TripSearchEngine().search(departure, destination, date)

        # then
        assert result == []

    @patch("app.domain.trips_api.TripsAPI.get_trips")
    def test_search_no_journeys_available(self, mock_get_trips):
        # given
        mock_get_trips.return_value = []
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = TripSearchEngine().search(departure, destination, date)

        # then
        assert result == []