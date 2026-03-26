import argparse 
import time
from datetime import datetime

from algorithms.dijkstra import dijkstra_search
from algorithms.a_star_time import astar_time_search
from algorithms.a_star_transits import astar_transits_search
from graph.TransitGraph import TransitGraph
from graph.loader import load_graph
from formatter import parse_path

def add_arguments(parser: argparse.ArgumentParser) -> None:
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

def main() -> None:
    
    parser = argparse.ArgumentParser(
        prog="AI labs - graph search",
        description="Go through a Lower Silesian train connections graph to find the best connection from point A to point B based on specified criteria."
    )

    add_arguments(parser)
    args = parser.parse_args()

    transit_graph: TransitGraph = load_graph()

    start_station_id = transit_graph.find_station_id_by_name(args.start)
    destination_station_id = transit_graph.find_station_id_by_name(args.destination)
    
    if args.algorithm == 'D':
        algorithm = dijkstra_search
    else: 
        if args.criterion == 't':
            algorithm = astar_time_search
        else:
            algorithm = astar_transits_search
    
    start_compute = time.time()
    print('Searching for the best path ...')

    path = algorithm(
        graph= transit_graph,
        start_station_id= start_station_id,
        destination_station_id= destination_station_id,
        start_time= args.time
    )

    print(f'The search took {round(time.time() - start_compute,2)}s')

    if path is None:
        print(f"No path connecting {args.start} and {args.destination} found")
        return

    parse_path(
        path=path,
        graph=transit_graph,
        query_start_time=args.time,
        query_start_name=args.start,
        query_destination_name=args.destination
    )

if __name__ == "__main__":
    main()