from datetime import datetime
from unittest.mock import patch, ANY

from freezegun import freeze_time

from app.domain.flight_search_engine import FlightSearchEngine


@freeze_time("2024-09-11")
class TestSearchEngine:
    # NOTE: I haven't tested the case of journeys from another date since I assume we can filter
    # the journeys by date from the API
    @patch("app.domain.flights_api.FlightsAPI.get_flights")
    def test_search_journeys_happy_path(self, mock_get_flights):
        # given
        mock_get_flights.return_value = [
            {
                "flight_number": "XX1234",
                "departure_city": "BUE",
                "arrival_city": "MAD",
                "departure_datetime": datetime(2024, 9, 11, 10, 0),
                "arrival_datetime": datetime(2024, 9, 11, 23, 0)
            }
        ]
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = FlightSearchEngine().search(departure, destination, date)

        # then
        assert result == [{"connections": 1, "path": [{"flight_number": "XX1234", "from": "BUE", "to": "MAD",
                                                       "departure_time": ANY,
                                                       "arrival_time": ANY}]}]

    @patch("app.domain.flights_api.FlightsAPI.get_flights")
    def test_search_journeys_with_combinations(self, mock_get_flights):
        # given
        mock_get_flights.return_value = [
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
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = FlightSearchEngine().search(departure, destination, date)

        # then
        assert result == [{"connections": 2,
                           "path": [
                               {"flight_number": "XX1234",
                                "from": "BUE",
                                "to": "MDQ",
                                "departure_time": ANY,
                                "arrival_time": ANY},
                               {"flight_number": "XX2234",
                                "from": "MDQ",
                                "to": "MAD",
                                "departure_time": ANY,
                                "arrival_time": ANY},
                           ]}]

    @patch("app.domain.flights_api.FlightsAPI.get_flights")
    def test_search_journeys_two_combinations_available(self, mock_get_flights):
        # given
        mock_get_flights.return_value = [
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
            },
            {
                "flight_number": "XX3234",
                "departure_city": "MDQ",
                "arrival_city": "MAD",
                "departure_datetime": datetime(2024, 9, 11, 15, 0),
                "arrival_datetime": datetime(2024, 9, 11, 17, 0)
            }
        ]
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = FlightSearchEngine().search(departure, destination, date)

        # then
        assert result == [{"connections": 2,
                           "path": [
                               {"flight_number": "XX1234",
                                "from": "BUE",
                                "to": "MDQ",
                                "departure_time": ANY,
                                "arrival_time": ANY},
                               {"flight_number": "XX2234",
                                "from": "MDQ",
                                "to": "MAD",
                                "departure_time": ANY,
                                "arrival_time": ANY},
                           ]},
                          {"connections": 2,
                           "path": [
                               {"flight_number": "XX1234",
                                "from": "BUE",
                                "to": "MDQ",
                                "departure_time": ANY,
                                "arrival_time": ANY},
                               {"flight_number": "XX3234",
                                "from": "MDQ",
                                "to": "MAD",
                                "departure_time": ANY,
                                "arrival_time": ANY},
                           ]}
                          ]

    @patch("app.domain.flights_api.FlightsAPI.get_flights")
    def test_search_journeys_only_one_journey_of_more_than_24_hs_available(self, mock_get_flights):
        # given
        mock_get_flights.return_value = [
            {
                "flight_number": "XX1234",
                "departure_city": "BUE",
                "arrival_city": "MAD",
                "departure_datetime": datetime(2024, 9, 11, 10, 0),
                "arrival_datetime": datetime(2024, 9, 12, 10, 1)
            },
        ]
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = FlightSearchEngine().search(departure, destination, date)

        # then
        assert result == []

    @patch("app.domain.flights_api.FlightsAPI.get_flights")
    def test_search_journeys_one_combinations_for_more_than_24_hs_available(self, mock_get_flights):
        # given
        mock_get_flights.return_value = [
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
                "arrival_datetime": datetime(2024, 9, 12, 10, 1)
            }
        ]
        departure = "BUE"
        destination = "MAD"
        date = datetime.now().date()

        # when
        result = FlightSearchEngine().search(departure, destination, date)

        # then
        assert result == []

    @patch("app.domain.flights_api.FlightsAPI.get_flights")
    def test_search_journeys_one_combination_with_a_connection_of_more_than_2_hs_available(self, mock_get_flights):
        # given
        mock_get_flights.return_value = [
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
                "departure_datetime": datetime(2024, 9, 11, 15, 1),
                "arrival_datetime": datetime(2024, 9, 12, 6, 0)
            }
        ]
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