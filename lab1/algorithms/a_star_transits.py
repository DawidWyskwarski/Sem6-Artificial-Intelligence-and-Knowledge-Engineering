import heapq
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional, List

from graph.TransitGraph import TransitGraph
from graph.Edge import Edge
from graph.Station import Station
from graph.Trip import Trip
from algorithms.utils import distance_heuristic, reconstruct_path, can_take_this_train, time_cost, transit_cost

def astar_transits_search(
    graph: TransitGraph,
    start_station_id: int,
    destination_station_id: int,
    start_time: datetime) -> Optional[List[Edge]]:
    
    destination_station: Station = graph.stations[destination_station_id]
    
    # Priority queue ordered by the smallest f-score first.
    queue = []
    
    start_h = distance_heuristic(
        station= graph.stations[start_station_id], 
        destination=destination_station
    )

    # State is now (station_id, trip_id) - trip_id=None means we haven't boarded yet.
    start_state = (start_station_id, None)
    # Queue entry: (f_score, g_score, time_cost, station_id, trip_id)
    # where f = g + h.
    heapq.heappush(queue, (start_h, 0.0, 0.0, start_station_id, None))
    
    # best_g_costs stores the best real travel cost discovered so far for each station.
    best_g_costs: dict = defaultdict(lambda: float('inf'))
    best_g_costs[start_state] = 0.0
    
    # Parent pointers for path reconstruction.
    came_from = {start_state: (None, None)}
    
    while queue:
    
        _, current_g, current_time_cost, current_station_id, current_trip_id = heapq.heappop(queue)
        
        current_state = (current_station_id, current_trip_id)

        # Ignore stale queue entries that are worse than the best known g-cost.
        if current_g > best_g_costs[current_state]:
            continue
    
        # Goal reached: rebuild and return the path.
        if current_station_id == destination_station_id:
            return _reconstruct_path(came_from=came_from, dest_state=current_state)

        current_time: datetime = start_time + timedelta(minutes=current_time_cost)
 
        # Get the edge we arrived on so transit_cost() can detect line changes.
        prev_edge, _ = came_from[current_state]

        for edge in graph.edges[current_station_id]:
            trip: Trip = graph.trips[edge.trip_id]
            
            # Skip edges that have no valid future departure for the current time.
            if not can_take_this_train(date=current_time, edge=edge, trip=trip):
                continue
            
            # Edge travel cost already includes waiting time + ride time.
            edge_time_cost = time_cost(
                current_datetime=current_time, 
                edge=edge, 
                trip=trip
            )
            edge_transit_cost = transit_cost(
                edge= edge,
                prev_edge= prev_edge if prev_edge else edge
            )

            # Tentative real cost from start to this neighbor.
            tentative_g = current_g + (edge_time_cost + edge_transit_cost)

            new_destination = edge.destination_stop_id
            new_state = (new_destination, edge.trip_id)

            next_station = graph.stations[new_destination]
            # Heuristic estimate from neighbor to goal.
            
            heur_cost = distance_heuristic(next_station, destination_station)
            
            tentative_f = tentative_g + heur_cost
            new_time_cost = edge_time_cost + current_time_cost

            # Standard A* relaxation step.
            if tentative_g < best_g_costs[new_state]:
                best_g_costs[new_state] = tentative_g
                came_from[new_state] = (edge, current_state)
                heapq.heappush(queue, (tentative_f, tentative_g, new_time_cost, new_destination, edge.trip_id))
    
    return None

def _reconstruct_path(came_from: dict, dest_state: tuple) -> List[Edge]:
    path: List[Edge] = []
    current_state = dest_state
    while True:
        edge, prev_state = came_from[current_state]
        if edge is None:
            break
        path.append(edge)
        current_state = prev_state
    path.reverse()
    return path