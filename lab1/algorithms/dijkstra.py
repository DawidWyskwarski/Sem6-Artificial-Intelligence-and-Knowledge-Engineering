import heapq
from datetime import datetime, time, timedelta
from collections.abc import Callable
from collections import defaultdict
from typing import Optional, List, Tuple

from graph.TransitGraph import TransitGraph
from graph.Edge import Edge
from graph.Trip import Trip
from graph.utils import can_take_this_train

class DijkstraAlgorithm:

    def search(
            self, 
            graph: TransitGraph,
            start_station_id: int,
            desitnation_station_id: int,
            start_time: datetime,
            fun_opt: Callable[[datetime, Edge, Trip], int]) -> Tuple[Optional[List[Edge]], float]:
        
        queue = []
        heapq.heappush(queue, (0, start_station_id))

        best_costs: dict = defaultdict(lambda: float('inf'))
        best_costs[start_station_id] = 0

        came_from = {start_station_id: None}

        while queue:
            current_cost, current_station_id = heapq.heappop(queue)

            current_time: datetime = start_time + timedelta(minutes=current_cost)

            if current_cost > best_costs[current_station_id]:
                continue

            if current_station_id == desitnation_station_id:
                return self._reconstruct_path(came_from, desitnation_station_id), current_cost
            
            for edge in graph.edges[current_station_id]:
                trip = graph.trips[edge.trip_id]
                
                if not can_take_this_train(current_time, edge, trip):
                    continue

                new_cost = fun_opt(current_time, edge, trip) + current_cost
                new_destination = edge.destination_stop_id

                if new_cost < best_costs[new_destination]:
                    best_costs[new_destination] = new_cost
                    came_from[new_destination] = edge
                    heapq.heappush(queue, (new_cost, new_destination))

        return None, -1
    

    def _reconstruct_path(
            self,
            came_from: dict,
            dest_id: int) -> List[Edge]:
        
        path: List[Edge] = []
        
        curr = dest_id

        while came_from[curr] is not None:
            edge = came_from[curr]

            path.append(edge)

            curr = edge.start_stop_id

        path.reverse()
        return path