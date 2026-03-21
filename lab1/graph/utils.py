from datetime import datetime, timedelta, time
from typing import Optional

from graph.Edge import Edge
from graph.Trip import Trip

def _departure_datetime_for_service_date(service_date, departure_time: int) -> datetime:
    midnight = datetime.combine(service_date, time.min)
    return midnight + timedelta(minutes=departure_time)

def next_departure_datetime(current_datetime: datetime, edge: Edge, trip: Trip) -> Optional[datetime]:

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
    return next_departure_datetime(date, edge, trip) is not None

def time_cost(current_datetime: datetime, edge: Edge, trip: Trip) -> float:
    departure_datetime = next_departure_datetime(current_datetime, edge, trip)
    
    # Shouldn't happen because we are checking in an algorithm
    if departure_datetime is None:
        return float('inf')
    
    waiting_minutes = int((departure_datetime - current_datetime).total_seconds() // 60)
    return waiting_minutes + edge.travel_time()