import argparse
import sys
from datetime import datetime, timedelta
import time

from graph.TransitGraph import TransitGraph
from graph.loader import loadGraph
from graph.utils import time_cost, next_departure_datetime
from algorithms.dijkstra import DijkstraAlgorithm
from graph.Edge import Edge
from typing import List

def add_arguments(parser: argparse.ArgumentParser):
    def parse_datetime(s):
        try:
            return datetime.strptime(s, "%d.%m.%Y %H:%M")
        except ValueError:
            try:
                return datetime.fromisoformat(s)
            except ValueError:
                raise argparse.ArgumentTypeError(f"Not a valid datetime: '{s}'. Expected format: 'DD.MM.YYYY HH:MM' or ISO format.")
    
    parser.add_argument('-a', '--algorithm', required=True, choices=['D', 'A*'], help="Algorithm to use ('D' for Dijkstra, 'A*' for A-Star)")
    parser.add_argument('-s', '--start', required=True, help="Starting station")
    parser.add_argument('-d', '--destination', required=True, help="Destination station")
    parser.add_argument('-t', '--time', required=True, type=parse_datetime, help="Departure time (e.g., '20.03.2026 14:30' or ISO format)")
    parser.add_argument('-c', '--criterion', choices=['t', 'p'], default='t', help="Optimization criterion ('t' for time, 'p' for price/transfers)")

def _format_duration(total_minutes: int) -> str:
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours}h {minutes:02d}m"

def parse_path(
        path: List[Edge],
        best_cost: int,
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
    print(f"Optimized cost:     {_format_duration(int(best_cost))}")

def main():
    parser = argparse.ArgumentParser(
        prog="AI labs - graph search",
        description="Go through a Lower Silesian train connections graph to find the best connection from point A to point B based on specified criteria."
    )

    add_arguments(parser)
    args = parser.parse_args()

    transit_graph: TransitGraph = loadGraph()

    start_station_id = transit_graph.find_station_id_by_name(args.start)
    destination_station_id = transit_graph.find_station_id_by_name(args.destination)
    
    if args.algorithm == 'D':
        algorithm = DijkstraAlgorithm()
        opt_fun = time_cost
    else: 
        raise NotImplementedError("Chill out man")
    
    start_compute = time.time()
    
    print('Searching for the best path ...')
    path, best_cost = algorithm.search(
        graph= transit_graph,
        start_station_id= start_station_id,
        desitnation_station_id= destination_station_id,
        start_time= args.time,
        fun_opt=opt_fun
    )
    print(f'The search took {round(time.time() - start_compute,2)}s')

    parse_path(
        path=path,
        best_cost=int(best_cost),
        graph=transit_graph,
        query_start_time=args.time,
        query_start_name=args.start,
        query_destination_name=args.destination
    )

if __name__ == "__main__":
    main()