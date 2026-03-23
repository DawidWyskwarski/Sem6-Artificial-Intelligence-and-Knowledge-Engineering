from datetime import datetime, timedelta, time
from typing import Optional, List
from math import sqrt

from graph.Edge import Edge
from graph.Trip import Trip
from graph.Station import Station

def _departure_datetime_for_service_date(service_date, departure_time: int) -> datetime:
    '''
    Transforms the GTFS format into datetime. Reason for this function is that `departure_time` can be larger than 24

    @param service_date: The date in which a given connection is active
    @param departure_time: Hour at wchich the train leaves the station. Can be larger than 24
    @return: exact point in time then the train leavs. Represented as a `datetime` 
    '''
    midnight = datetime.combine(service_date, time.min)
    return midnight + timedelta(minutes=departure_time)

def next_departure_datetime(current_datetime: datetime, edge: Edge, trip: Trip) -> Optional[datetime]:
    '''
    Finds the closest `datetime` on which the connection is active

    @param current_datetime: date and time for which we calculate the next date
    @param edge: the connection that we check
    @param trip: `Trip` object that the `edge` is assigned to. Contains neccessary info about schedule.
    @return: `Optional[datetime]` return next datetime on which edge is active. Returns None if such connection is closed for good. 

    '''
    
    # Find an earliest valid date where the trip could be active
    candidate_service_date = (current_datetime - timedelta(minutes=edge.departure_time)).date()
    candidate_departure = _departure_datetime_for_service_date(candidate_service_date, edge.departure_time)
    if candidate_departure < current_datetime:
        candidate_service_date += timedelta(days=1)

    upper_bound = trip.finish_date
    if trip.added_days:
        upper_bound = max(upper_bound, max(trip.added_days))

    while candidate_service_date <= upper_bound:
        if trip.is_active(candidate_service_date):
            return _departure_datetime_for_service_date(candidate_service_date, edge.departure_time)
        candidate_service_date += timedelta(days=1)

    return None

def can_take_this_train(date: datetime, edge: Edge, trip: Trip) -> bool:
    '''
    Check if there is a date in the future on wchich we can take the connection.
    It just checks if the output from `next_departure_datetime` is not None
    '''
    return next_departure_datetime(date, edge, trip) is not None

def time_cost(current_datetime: datetime, edge: Edge, trip: Trip) -> float:
    '''
    Calculates time cost neccessary to use this edge. waiting time + travel time
    '''
    
    departure_datetime = next_departure_datetime(current_datetime, edge, trip)
    
    # Shouldn't happen because we are checking in an algorithm
    if departure_datetime is None:
        return float('inf')
    
    waiting_minutes = int((departure_datetime - current_datetime).total_seconds() // 60)
    return waiting_minutes + edge.travel_time()


# Must be larger than the longest possible journey in the network (in minutes)
# to ensure transfer count always dominates over travel time in the g-score.
# ~16h is a safe upper bound for Lower Silesia.
TRANSIT_COST = 1_000

def transit_cost(edge: Edge, prev_edge: Edge) -> float:
    return TRANSIT_COST if edge.trip_id != prev_edge.trip_id else 0


def reconstruct_path(
    came_from: dict,
    dest_id: int) -> List[Edge]:
    '''
    Based on dictionary from algorithm reconstructs the best found path by going backwards from the destination to the start station.

    @param came_from: dictionary mapping stations to edges that we got there
    @param dest_id: id of destination station
    @return: list of edges from starting station to destination
    '''

    path: List[Edge] = []
    
    curr = dest_id
    while came_from[curr] is not None:
        edge = came_from[curr]
        path.append(edge)
        curr = edge.start_stop_id
    path.reverse()
    return path

# Constants for changing degree distance to minutes
MAX_SPEED_KMH = 140.0
DEGREE_TO_KM_RATIO = 111.0

def distance_heuristic(
    station: Station, 
    destination: Station) -> float:
    '''
    Calculate the approximate time to get from the station to destination in a straight line. As a avg max speed of a trin `MAX_SPEED_KMH` was used

    @param station: stataion from which we calculate distance
    @param destination: station to which we calculate distance  
    '''

    dlat = destination.lat - station.lat
    dlon = destination.lon - station.lon

    dist_deg = sqrt(dlat * dlat + dlon * dlon)
    dist_km = dist_deg * DEGREE_TO_KM_RATIO
    
    return (dist_km / MAX_SPEED_KMH) * 60.0