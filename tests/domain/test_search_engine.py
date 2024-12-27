from datetime import datetime
from unittest.mock import patch, ANY

from freezegun import freeze_time

from app.domain.flight_search_engine import FlightSearchEngine
from tests.fixtures import *


@freeze_time("2024-09-11")
class TestSearchEngine:
    # NOTE: I haven't tested the case of journeys from another date since I assume we can filter
    # the journeys by date from the API
    @patch("app.domain.flights_api.FlightsAPI.get_flights")
    def test_search_journeys_happy_path(self, mock_get_flights, one_flight_journey_combination):
        # given
        mock_get_flights.return_value = one_flight_journey_combination
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = FlightSearchEngine().search(departure, destination, date)

        # then
        assert result == [{"connections": 1, "path": [{"flight_number": "XX1234", "from_": "BUE", "to": "MAD",
                                                       "departure_time": ANY,
                                                       "arrival_time": ANY}]}]

    @patch("app.domain.flights_api.FlightsAPI.get_flights")
    def test_search_journeys_with_combinations(self, mock_get_flights, two_flights_journey_combination):
        # given
        mock_get_flights.return_value = two_flights_journey_combination
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = FlightSearchEngine().search(departure, destination, date)

        # then
        assert result == [{"connections": 2,
                           "path": [
                               {"flight_number": "XX1234",
                                "from_": "BUE",
                                "to": "MDQ",
                                "departure_time": ANY,
                                "arrival_time": ANY},
                               {"flight_number": "XX2234",
                                "from_": "MDQ",
                                "to": "MAD",
                                "departure_time": ANY,
                                "arrival_time": ANY},
                           ]}]

    @patch("app.domain.flights_api.FlightsAPI.get_flights")
    def test_search_journeys_one_destination_that_does_not_match(self, mock_get_flights, one_flight_journey_combination_with_another_destiny):
        # given
        mock_get_flights.return_value = one_flight_journey_combination_with_another_destiny
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = FlightSearchEngine().search(departure, destination, date)

        # then
        assert result == []

    @patch("app.domain.flights_api.FlightsAPI.get_flights")
    def test_search_journeys_one_origin_that_does_not_match(self, mock_get_flights, one_flight_journey_combination_of_two_flights_with_another_destiny):
        # given
        mock_get_flights.return_value = one_flight_journey_combination_of_two_flights_with_another_destiny
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = FlightSearchEngine().search(departure, destination, date)

        # then
        assert result == []

    @patch("app.domain.flights_api.FlightsAPI.get_flights")
    def test_search_journeys_two_combinations_available(self, mock_get_flights, multiple_flight_combinations):
        # given
        mock_get_flights.return_value = multiple_flight_combinations
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = FlightSearchEngine().search(departure, destination, date)

        # then
        assert result == [{"connections": 2,
                           "path": [
                               {"flight_number": "XX1234",
                                "from_": "BUE",
                                "to": "MDQ",
                                "departure_time": ANY,
                                "arrival_time": ANY},
                               {"flight_number": "XX2234",
                                "from_": "MDQ",
                                "to": "MAD",
                                "departure_time": ANY,
                                "arrival_time": ANY},
                           ]},
                          {"connections": 2,
                           "path": [
                               {"flight_number": "XX1234",
                                "from_": "BUE",
                                "to": "MDQ",
                                "departure_time": ANY,
                                "arrival_time": ANY},
                               {"flight_number": "XX3234",
                                "from_": "MDQ",
                                "to": "MAD",
                                "departure_time": ANY,
                                "arrival_time": ANY},
                           ]}
                          ]

    @patch("app.domain.flights_api.FlightsAPI.get_flights")
    def test_search_journeys_only_one_journey_of_more_than_24_hs_available(self, mock_get_flights, one_flight_for_total_more_than_24_hours):
        # given
        mock_get_flights.return_value = one_flight_for_total_more_than_24_hours
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = FlightSearchEngine().search(departure, destination, date)

        # then
        assert result == []

    @patch("app.domain.flights_api.FlightsAPI.get_flights")
    def test_search_journeys_one_combinations_for_more_than_24_hs_available(self, mock_get_flights, two_flights_for_total_more_than_24_hours):
        # given
        mock_get_flights.return_value = two_flights_for_total_more_than_24_hours
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = FlightSearchEngine().search(departure, destination, date)

        # then
        assert result == []

    @patch("app.domain.flights_api.FlightsAPI.get_flights")
    def test_search_journeys_one_combination_with_a_connection_of_more_than_4_hs_available(self, mock_get_flights,
                                                                                           flights_with_a_big_connection):
        # given
        mock_get_flights.return_value = flights_with_a_big_connection
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = FlightSearchEngine().search(departure, destination, date)

        # then
        assert result == []

    @patch("app.domain.flights_api.FlightsAPI.get_flights")
    def test_search_no_journeys_available(self, mock_get_flights):
        # given
        mock_get_flights.return_value = []
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = FlightSearchEngine().search(departure, destination, date)

        # then
        assert result == []