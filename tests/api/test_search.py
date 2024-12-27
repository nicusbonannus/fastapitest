from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from freezegun import freeze_time
from unittest.mock import patch, ANY

from app.main import app
from tests.fixtures import two_flights_journey_combination

client = TestClient(app)


@freeze_time("2024-09-11")
class TestGetJourneysAPI:
    @patch("app.domain.flights_api.FlightsAPI.get_flights")
    def test_get_journeys_happy_path(self, mock_get_flights, two_flights_journey_combination):
        # given
        mock_get_flights.return_value = two_flights_journey_combination
        search_parameters = {"departure": "BUE", "destination": "MAD", "date": datetime.now().date()}

        # when
        response = client.get("/journeys/search", params=search_parameters)

        # then
        assert response.status_code == 200
        assert response.json() == [
            {'connections': 2,
             'path': [
                 {
                     'arrival_time': '2024-09-11T13:00:00',
                     'departure_time': '2024-09-11T10:00:00',
                     'flight_number': 'XX1234',
                     'from_': 'BUE',
                     'to': 'MDQ'},
                 {
                     'arrival_time': '2024-09-11T16:00:00',
                     'departure_time': '2024-09-11T14:00:00',
                     'flight_number': 'XX2234',
                     'from_': 'MDQ',
                     'to': 'MAD'}
             ]}]

    def test_get_journeys__departure_with_more_than_3_chars_failed(self):
        # given
        search_parameters = {"departure": "BUEX", "destination": "MAD", "date": datetime.now().date()}

        # when
        response = client.get("/journeys/search", params=search_parameters)

        # then
        assert response.status_code == 422
        error_details = response.json()['detail'][0]
        assert 'departure' in error_details['loc']
        assert error_details['msg'] == 'String should have at most 3 characters'

    def test_get_journeys__destination_with_more_than_3_chars_failed(self):
        # given
        search_parameters = {"departure": "BUE", "destination": "MADMAX", "date": datetime.now().date()}

        # when
        response = client.get("/journeys/search", params=search_parameters)

        # then
        assert response.status_code == 422
        error_details = response.json()['detail'][0]
        assert 'destination' in error_details['loc']
        assert error_details['msg'] == 'String should have at most 3 characters'

    def test_get_journeys__date_in_the_past_failed(self):
        # given
        yesterday = datetime.now().date() - timedelta(days=1)
        search_parameters = {"departure": "BUE", "destination": "MAD", "date": yesterday}

        # when
        response = client.get("/journeys/search", params=search_parameters)

        # then
        assert response.status_code == 422
        assert response.json()['detail'] == 'Date cannot be in the past'

    def test_get_journeys__departure_field_not_included_failed(self):
        # given
        search_parameters = {"destination": "MAD", "date": datetime.now().date()}

        # when
        response = client.get("/journeys/search", params=search_parameters)

        # then
        self._check_missing_field_was_validated(expected_field='departure', response=response)

    def test_get_journeys__destination_field_not_included_failed(self):
        # given
        search_parameters = {"departure": "MAD", "date": datetime.now().date()}

        # when
        response = client.get("/journeys/search", params=search_parameters)

        # then
        self._check_missing_field_was_validated(expected_field='destination', response=response)

    def test_get_journeys__date_field_not_included_failed(self):
        # given
        search_parameters = {"destination": "MAD", "departure": "BUE"}

        # when
        response = client.get("/journeys/search", params=search_parameters)

        # then
        self._check_missing_field_was_validated(expected_field='date', response=response)

    def _check_missing_field_was_validated(self, expected_field, response):
        assert response.status_code == 422
        error_details = response.json()['detail'][0]
        assert expected_field in error_details['loc']
        assert error_details['msg'] == 'Field required'
