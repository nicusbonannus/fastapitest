from datetime import datetime, timedelta

import requests


class FlightsAPI:
    def get_flights(self, departure: str, date: datetime.date):

        # Some assumptions here since I don't have all the information about this API.
        # I am assuming that you can send a date range to the API to retrieve less entries.
        # I am assuming that the endpoint is not paginated to make the challenge simpler and more focused on the problem.
        # I am assuming the other API is external and does not have any authentication.

        url = "https://api.example.com/endpoint"
        next_day = date + timedelta(days=1)
        params = dict(date_gte=date, date_lte=next_day)
        response = requests.get(url, params=params)

        return response.json()
