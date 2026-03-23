import heapq
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional, List

from graph.TransitGraph import TransitGraph
from graph.Edge import Edge
from graph.Trip import Trip
from graph.Station import Station
from algorithms.utils import (
    can_take_this_train, reconstruct_path, 
    distance_heuristic, time_cost
)

def astar_time_search(
        graph: TransitGraph,
        start_station_id: int,
        destination_station_id: int,
        start_time: datetime) -> Optional[List[Edge]]:
    
    # Destination station is needed to evaluate heuristic distance-to-goal.
    destination_station: Station = graph.stations[destination_station_id]
    
    # Priority queue ordered by the smallest f-score first.
    queue = []
    
    start_h = distance_heuristic(
        station= graph.stations[start_station_id], 
        destination=destination_station
    )

    # Queue state: (f_score, g_score, station_id)
    # where f = g + h.
    heapq.heappush(queue, (start_h, 0.0, start_station_id))
    
    # best_g_costs stores the best real travel cost discovered so far for each station.
    best_g_costs: dict = defaultdict(lambda: float('inf'))
    best_g_costs[start_station_id] = 0.0
    
    # Parent pointers for path reconstruction.
    came_from = {start_station_id: None}
    
    while queue:
    
        _, current_g, current_station_id = heapq.heappop(queue)
        current_time: datetime = start_time + timedelta(minutes=current_g)
    
        # Ignore stale queue entries that are worse than the best known g-cost.
        if current_g > best_g_costs[current_station_id]:
            continue
    
        # Goal reached: rebuild and return the path.
        if current_station_id == destination_station_id:
            return reconstruct_path(came_from=came_from, dest_id=destination_station_id)
    
        for edge in graph.edges[current_station_id]:
            trip: Trip = graph.trips[edge.trip_id]
            
            # Skip edges that have no valid future departure for the current time.
            if not can_take_this_train(date=current_time, edge=edge, trip=trip):
                continue
            
            # Edge travel cost already includes waiting time + ride time.
            edge_cost = time_cost(
                current_datetime=current_time, 
                edge=edge, 
                trip=trip
            )
            
            # Tentative real cost from start to this neighbor.
            tentative_g = current_g + edge_cost

            new_destination = edge.destination_stop_id
            
            next_station = graph.stations[new_destination]
            # Heuristic estimate from neighbor to goal.
            heur_cost = distance_heuristic(next_station, destination_station)
            
            tentative_f = tentative_g + heur_cost
            
            # Standard A* relaxation step.
            if tentative_g < best_g_costs[new_destination]:
                best_g_costs[new_destination] = tentative_g
                came_from[new_destination] = edge
                heapq.heappush(queue, (tentative_f, tentative_g, new_destination))
    
    return None