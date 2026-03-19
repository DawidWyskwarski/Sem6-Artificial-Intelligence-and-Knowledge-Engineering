from dataclasses import dataclass
from Trip import Trip
from datetime import date

@dataclass
class Edge:
    # Where we are going from
    start_stop_id: int
    # Where we are going to
    destination_stop_id: int
    # Calculate const when optimizing for time
    arrival_time: float
    departure_time: float
    # Based on this we will take the Trip object from TransitGraph 
    # to calculate active state of the edge
    # Also calculate cost when optimizing for number of changes
    trip_id: int 

    # Calculates wether we can chose this route on a given date
    def is_active(self, run_date: date, trip: Trip) -> bool:
        if run_date in trip.added_days:
            return True
        
        if run_date in trip.removed_days:
            return False
        
        if run_date <= trip.finish_date and run_date >= trip.start_date:
            return trip.weekdays[run_date.weekday()]
        
        return False