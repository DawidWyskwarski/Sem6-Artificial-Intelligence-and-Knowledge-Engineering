from typing import Dict, List
from Station import Station
from Edge import Edge
from Trip import Trip

# Class coordinating the entire structure
class TransitGraph:
    def __init__(self):
        # Key is station_id 
        # Value is a corresponding Station object
        self.stations: Dict[int, Station] = {}
        # Key is a station_id
        # Value is a collection of Connections to other Stations
        self.edges: Dict[int, List[Edge]] = {}
        # Key is trip_id
        # Value is a corresponding Trip object
        # Mainly here to check wether an Edge is active or not on a given date
        self.trips: Dict[int, Trip] = {}
        # Maps raw stop_ids (platforms) to their parent station_ids
        self.stop_id_mapping: Dict[int, int] = {}

    def add_station(self, station: Station):
        self.stations[station.station_id] = station
        
        if station.station_id not in self.edges:
            self.edges[station.station_id] = []

    def add_edge(self, edge: Edge):
        self.edges[edge.start_stop_id].append(edge)

    def add_trip(self, trip: Trip):
        self.trips[trip.trip_id] = trip