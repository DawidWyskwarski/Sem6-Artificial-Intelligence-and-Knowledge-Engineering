from typing import Dict, List, Optional

from graph.Station import Station
from graph.Edge import Edge
from graph.Trip import Trip


class TransitGraph:
    def __init__(self):
        # Key: station_id  →  Station object
        self.stations: Dict[int, Station] = {}
        # Key: station_id  →  list of outgoing Edges
        self.edges: Dict[int, List[Edge]] = {}
        # Key: trip_id  →  Trip object (used to check schedule activity)
        self.trips: Dict[int, Trip] = {}
        # Maps raw stop_id (platform) → parent station_id
        self.stop_id_mapping: Dict[int, int] = {}

    def add_station(self, station: Station) -> None:
        self.stations[station.station_id] = station
        if station.station_id not in self.edges:
            self.edges[station.station_id] = []

    def add_edge(self, edge: Edge) -> None:
        self.edges[edge.start_stop_id].append(edge)

    def add_trip(self, trip: Trip) -> None:
        self.trips[trip.trip_id] = trip

    def find_station_id_by_name(self, station_name: str) -> Optional[int]:
        name_lower = station_name.strip().lower()
        for station_id, station in self.stations.items():
            if station.name.strip().lower() == name_lower:
                return station_id

        raise AttributeError(f"No station named '{station_name}' found in the graph")