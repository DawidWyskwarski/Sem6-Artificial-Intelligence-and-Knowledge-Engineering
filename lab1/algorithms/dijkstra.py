import heapq
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional, List

from graph.TransitGraph import TransitGraph
from graph.Edge import Edge
from algorithms.utils import can_take_this_train, reconstruct_path, time_cost

def dijkstra_search(
    graph: TransitGraph,
    start_station_id: int,
    destination_station_id: int,
    start_time: datetime) -> Optional[List[Edge]]:
    
    # priority queue -> using heapq module
    # minimal cost is always on top
    queue = []

    heapq.heappush(queue, (0, start_station_id))
    
    best_costs: dict = defaultdict(lambda: float('inf'))
    best_costs[start_station_id] = 0
    
    came_from = {start_station_id: None}
    
    while queue:
        current_cost, current_station_id = heapq.heappop(queue)

        # datetime at which we arrived at a given station 
        current_time: datetime = start_time + timedelta(minutes=current_cost)

        # If we already found better way to get to this station we skip it. 
        if current_cost > best_costs[current_station_id]:
            continue
        
        # If destination was found we return it
        if current_station_id == destination_station_id:
            return reconstruct_path(came_from, destination_station_id)
        
        for edge in graph.edges[current_station_id]:
        
            trip = graph.trips[edge.trip_id]

            # Some connections may not be available when we are having our trip
            if not can_take_this_train(current_time, edge, trip):
                continue
            
            new_cost = time_cost(current_time, edge, trip) + current_cost
            next_station_id = edge.destination_stop_id

            # if we find better way to get to a given station we update best_costs, came_from and push new edge to the queue
            if new_cost < best_costs[next_station_id]:
                best_costs[next_station_id] = new_cost
                came_from[next_station_id] = edge
                heapq.heappush(queue, (new_cost, next_station_id))

    return None
