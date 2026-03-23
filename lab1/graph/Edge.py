from dataclasses import dataclass

@dataclass
class Edge:
    # Where we are going from
    start_stop_id: int
    # Where we are going to
    destination_stop_id: int
    # Minutes from service-day midnight (can be >= 1440 for after-midnight GTFS times)
    arrival_time: int
    departure_time: int
    # Based on this we will take the Trip object from TransitGraph 
    # to calculate active state of the edge
    # Also calculate cost when optimizing for number of changes
    trip_id: int 

    def travel_time(self) -> int:
        return self.arrival_time - self.departure_time    