from datetime import timedelta, datetime
from typing import List

from algorithms.utils import next_departure_datetime
from graph.Edge import Edge
from graph.TransitGraph import TransitGraph

def _format_duration(total_minutes: int) -> str:
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours}h {minutes:02d}m"

def parse_path(
    path: List[Edge],
    graph: TransitGraph,
    query_start_time: datetime,
    query_start_name: str,
    query_destination_name: str) -> None:

    if path is None:
        print(f"No path was found connecting {query_start_name} and {query_destination_name}.")
        return

    print("\n" + "=" * 28)
    print("       BEST ROUTE")
    print("=" * 28)

    current_dt = query_start_time
    total_wait_minutes = 0
    total_ride_minutes = 0
    transfers = 0
    previous_trip_id = None
    first_departure_dt = None
    final_arrival_dt = None

    for idx, edge in enumerate(path, start=1):
        trip = graph.trips[edge.trip_id]
        departure_dt = next_departure_datetime(current_dt, edge, trip)

        if departure_dt is None:
            print("Path reconstruction error: a segment has no valid future departure.")
            return

        wait_minutes = int((departure_dt - current_dt).total_seconds() // 60)
        ride_minutes = edge.travel_time()
        arrival_dt = departure_dt + timedelta(minutes=ride_minutes)

        if previous_trip_id is not None and previous_trip_id != edge.trip_id:
            transfers += 1

        if first_departure_dt is None:
            first_departure_dt = departure_dt

        final_arrival_dt = arrival_dt
        total_wait_minutes += wait_minutes
        total_ride_minutes += ride_minutes
        previous_trip_id = edge.trip_id

        start_name = graph.stations[edge.start_stop_id].name
        end_name = graph.stations[edge.destination_stop_id].name

        print(
            f"{idx:02d}. [{departure_dt.strftime('%d.%m %H:%M')}] {start_name} "
            f"-> [{arrival_dt.strftime('%d.%m %H:%M')}] {end_name} | "
            f"Line: {trip.route_name}"
        )

        current_dt = arrival_dt

    if final_arrival_dt is None or first_departure_dt is None:
        print("Path is empty.")
        return

    total_journey_minutes = int((final_arrival_dt - query_start_time).total_seconds() // 60)

    print("\n" + "=" * 28)
    print("       STATISTICS")
    print("=" * 28)
    print(f"From:               {query_start_name}")
    print(f"To:                 {query_destination_name}")
    print(f"Requested start:    {query_start_time.strftime('%d.%m.%Y %H:%M')}")
    print(f"First departure:    {first_departure_dt.strftime('%d.%m.%Y %H:%M')}")
    print(f"Arrival:            {final_arrival_dt.strftime('%d.%m.%Y %H:%M')}")
    print(f"Total duration:     {_format_duration(total_journey_minutes)}")
    print(f"Ride time:          {_format_duration(total_ride_minutes)}")
    print(f"Waiting time:       {_format_duration(total_wait_minutes)}")
    print(f"Segments:           {len(path)}")
    print(f"Transfers:          {transfers}")