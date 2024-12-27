from collections import defaultdict
from datetime import datetime
from typing import List, Dict

from app.domain.flights_api import FlightsAPI


class FlightSearchEngine:
    MAX_JOURNEY_TIME_IN_SECONDS = 24 * 60 * 60
    MAX_CONNECTION_TIME_IN_SECONDS = 2 * 60 * 60
    def search(self, departure: str, destination: str, date: datetime.date):
        available_flights = FlightsAPI().get_flights(departure, date)
        matched_flights = self._filter_flights(available_flights, departure, destination)
        return [self._parse_journey(journey) for journey in matched_flights]

    def _is_flight_length_valid(self, flight) -> bool:
        journey_length = (flight['arrival_datetime'] - flight['departure_datetime']).total_seconds()
        return journey_length <= self.MAX_JOURNEY_TIME_IN_SECONDS

    def _is_flight_path_length_valid(self, path) -> bool:
        journey_length = (path[-1]['arrival_datetime'] - path[0]['departure_datetime']).total_seconds()
        return journey_length <= self.MAX_JOURNEY_TIME_IN_SECONDS

    def _is_connection_length_valid(self, path) -> bool:
        if len(path) <= 1:
            return True
        connection_length = (path[-1]['departure_datetime'] - path[-2]['arrival_datetime']).total_seconds()
        return connection_length <= self.MAX_CONNECTION_TIME_IN_SECONDS

    def _filter_flights(self, available_flights, departure, destination, max_connections=2) -> List[Dict]:
        """
        This method look for combinations of journeys that match with the departure and destination
        NOTE: This method is recursivity to escalate the number of connections in the future as state on the exercise
        :param available_flights: List of flights available for a particular date range
        :param departure: Code of the departure airport
        :param destination: Code of the destination airport
        :param max_connections: Optional: amount of connections allowed, 2 by default
        :return: List[Dict] with the combinations of flights that match with the departure and destination
        """
        connections = self._organize_connections(available_flights)
        for flight in connections[departure]:
            if flight["arrival_city"] == destination:
                if self._is_flight_length_valid(flight):
                    yield {"flights": [flight]}
                return

        def _search_connection(current_city, path, visited_cities):
            if not self._is_connection_length_valid(path):
                return
            if current_city == destination:
                if self._is_flight_path_length_valid(path):
                    yield {"flights": path}
                return
            if len(path) >= max_connections:
                return

            for flight in connections[current_city]:
                next_destiny = flight["arrival_city"]
                if next_destiny not in visited_cities:
                    yield from _search_connection(next_destiny, path + [flight], visited_cities | {next_destiny})
        yield from _search_connection(departure, [], {departure})

    def _organize_connections(self, available_flights):
        connections = defaultdict(list)
        for flight in available_flights:
            connections[flight["departure_city"]].append(flight)
        return connections

    def _parse_journey(self, journey):
        return {
            "connections": len(journey["flights"]),
            "path": [
                {
                    "flight_number" : flight["flight_number"],
                    "from_": flight["departure_city"],
                    "to": flight["arrival_city"],
                    "departure_time": flight["departure_datetime"],
                    "arrival_time": flight["arrival_datetime"]

                } for flight in journey["flights"]
            ]
        }


