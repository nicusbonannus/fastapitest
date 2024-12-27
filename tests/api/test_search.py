from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestGetJourneysAPI:
    current_date = None

    @classmethod
    def setup_class(cls):
        cls.current_date = datetime.now().date()

    def test_get_journeys_happy_path(self):
        # given
        search_parameters = {"departure": "BUE", "destination": "MAD", "date": self.current_date}

        # when
        response = client.get("/journeys/search", params=search_parameters)

        # then
        assert response.status_code == 200
        assert response.json() == [{"connections": 2, "path": [{"flight_number": "XX1234", "from": "BUE", "to": "MAD",
        "departure_time": "2024-09-12 00:00", "arrival_time": "2024-09-13 00:00"}]}]


    def test_get_journeys__departure_with_more_than_3_chars_failed(self):
        # given
        search_parameters = {"departure": "BUEX", "destination": "MAD", "date": self.current_date}

        # when
        response = client.get("/journeys/search", params=search_parameters)

        # then
        assert response.status_code == 422
        error_details = response.json()['detail'][0]
        assert 'departure' in error_details['loc']
        assert error_details['msg'] == 'String should have at most 3 characters'


    def test_get_journeys__destination_with_more_than_3_chars_failed(self):
        # given
        search_parameters = {"departure": "BUE", "destination": "MADMAX", "date": self.current_date}

        # when
        response = client.get("/journeys/search", params=search_parameters)

        # then
        assert response.status_code == 422
        error_details = response.json()['detail'][0]
        assert 'destination' in error_details['loc']
        assert error_details['msg'] == 'String should have at most 3 characters'


    def test_get_journeys__date_in_the_past_failed(self):
        # given
        yesterday = self.current_date - timedelta(days=1)
        search_parameters = {"departure": "BUE", "destination": "MAD", "date": yesterday}

        # when
        response = client.get("/journeys/search", params=search_parameters)

        # then
        assert response.status_code == 422
        assert response.json()['detail'] == 'Date cannot be in the past'


    def test_get_journeys__departure_field_not_included_failed(self):
        # given
        search_parameters = {"destination": "MAD", "date": self.current_date}

        # when
        response = client.get("/journeys/search", params=search_parameters)

        # then
        self._check_missing_field_was_validated(expected_field='departure', response=response)


    def test_get_journeys__destination_field_not_included_failed(self):
        # given
        search_parameters = {"departure": "MAD", "date": self.current_date}

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
