from datetime import datetime, timedelta

import requests


class TripsAPI:
    def get_trips(self, departure: str, date: datetime.date):
        url = "https://api.example.com/endpoint"
        next_day = date + timedelta(days=1)
        params = dict(date_gte=date, date_lte=next_day)
        response = requests.get(url, params=params)

        return response.json()
