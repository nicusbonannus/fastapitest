from collections import defaultdict
from datetime import datetime
from tokenize import triple_quoted, StringPrefix
from typing import List, Dict

from app.domain.trips_api import TripsAPI


class TripSearchEngine:
    MAX_JOURNEY_TIME_IN_SECONDS = 24 * 60 * 60 # 24 hours
    MAX_CONNECTION_TIME_IN_SECONDS = 4 * 60 * 60 # 4 hours
    def search(self, departure: str, destination: str, date: datetime.date):
        available_trips = TripsAPI().get_trips(departure, date)
        matched_trips = self._filter_trips(available_trips, departure, destination)
        return [self._parse_journey(journey) for journey in matched_trips]

    def _is_trip_length_valid(self, trip) -> bool:
        journey_length = (trip['arrival_datetime'] - trip['departure_datetime']).total_seconds()
        return journey_length <= self.MAX_JOURNEY_TIME_IN_SECONDS

    def _is_trip_path_length_valid(self, path) -> bool:
        journey_length = (path[-1]['arrival_datetime'] - path[0]['departure_datetime']).total_seconds()
        return journey_length <= self.MAX_JOURNEY_TIME_IN_SECONDS

    def _is_connection_length_valid(self, path) -> bool:
        if len(path) <= 1:
            return True
        connection_length = (path[-1]['departure_datetime'] - path[-2]['arrival_datetime']).total_seconds()
        return connection_length <= self.MAX_CONNECTION_TIME_IN_SECONDS

    def _filter_trips(self, available_trips, departure, destination, max_connections=2) -> List[Dict]:
        """
        This method look for combinations of journeys that match with the departure and destination
        :param available_trips: List of trips available for a particular date range
        :param departure: Code of the departure city
        :param destination: Code of the destination city
        :param max_connections: Optional: amount of connections allowed, 2 by default
        :return: List[Dict] with the combinations of trips that match with the departure and destination
        """
        connections = self._organize_connections(available_trips)
        for trip in connections[departure]:
            if trip["arrival_city"] == destination:
                if self._is_trip_length_valid(trip):
                    yield {"trips": [trip]}
                return

        def _search_connection(current_city, path, visited_cities):
            if not self._is_connection_length_valid(path):
                return
            if current_city == destination:
                if self._is_trip_path_length_valid(path):
                    yield {"trips": path}
                return
            if len(path) >= max_connections:
                return

            for trip in connections[current_city]:
                next_destiny = trip["arrival_city"]
                if next_destiny not in visited_cities:
                    yield from _search_connection(next_destiny, path + [trip], visited_cities | {next_destiny})
        yield from _search_connection(departure, [], {departure})

    def _organize_connections(self, available_trips):
        connections = defaultdict(list)
        for trip in available_trips:
            connections[trip["departure_city"]].append(trip)
        return connections

    def _parse_journey(self, journey):
        return {
            "connections": len(journey["trips"]),
            "path": [
                {
                    "trip_number" : trip["trip_number"],
                    "from_": trip["departure_city"],
                    "to": trip["arrival_city"],
                    "departure_time": trip["departure_datetime"],
                    "arrival_time": trip["arrival_datetime"]

                } for trip in journey["trips"]
            ]
        }


