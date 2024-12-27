from datetime import datetime

from app.domain.flights_api import FlightsAPI


class FlightSearchEngine:
    def search(self, departure: str, destination: str, date: datetime.date):
        available_flights = FlightsAPI().get_flights(departure, date)

        matched_flights = self._filter_flights(available_flights, departure, destination, date)

        # Recorrer cada vuelo
        # si el vuelo tiene el mismo destino y salida, verificar solo la duracion
        # Si el vuelo tiene otro destino y salida, skip
        # usar un generator
        # si el vuelo tiene la misma salida y otro destino, recorrer los otros vuelos e ir agregando por cada match a la lista
        # verificar para este caso la duracion de la escala y la dureacion total


        return [self._parse_journey(journey) for journey in matched_flights]

    def _filter_flights(self, available_flights, departure, destination, date):
        for flight in available_flights:
            flight_option = None
            flight_length = None
            if flight["departure_city"] == departure and flight["arrival_city"] == destination:
                flight_option =  {"flights": [flight]}
                flight_length = flight["arrival_datetime"] - flight["departure_datetime"]
                yield flight_option
            if flight["departure_city"] == departure and flight["arrival_city"] != destination:
                for next_flight in available_flights:
                    if flight["arrival_city"] == next_flight["departure_city"] and next_flight["arrival_city"] == destination:
                        connection_delay = next_flight["departure_datetime"] - flight["arrival_datetime"]
                        if connection_delay.seconds < 4*60*60:
                            yield {"flights": [flight, next_flight]}
                            flight_length = next_flight["arrival_datetime"] - flight["departure_datetime"]
            # if flight_option is None:
            #     continue
            # if flight_length.seconds > 24*60*60:
            #     continue
            # yield flight_option

    def _parse_journey(self, journey):
        return {
            "connections": len(journey["flights"]),
            "path": [
                {
                    "flight_number" : flight["flight_number"],
                    "from": flight["departure_city"],
                    "to": flight["arrival_city"],
                    "departure_time": flight["departure_datetime"],
                    "arrival_time": flight["arrival_datetime"]

                } for flight in journey["flights"]
            ]
        }


