import pandas as pd
import time
from datetime import date

from graph.TransitGraph import TransitGraph
from graph.Station import Station
from graph.Trip import Trip
from graph.Edge import Edge

DATA_PATH = './data/csv/'

def _load_stations(
    graph: TransitGraph, 
    stops_file_name: str) -> None:
    
    stations_df = pd.read_csv(DATA_PATH + stops_file_name)

    for row in stations_df.itertuples():
        raw_stop_id = int(row.stop_id)
        # I don't want to account for platforms 
        # So i won't do that
        # We just take the parent_station_id
        if pd.isna(row.parent_station):
            station_id = raw_stop_id
        else:
            station_id = int(row.parent_station)
        
        # Howeever we need to map the child stations (platforms)
        graph.stop_id_mapping[raw_stop_id] = station_id
        
        station = Station(
            station_id=station_id,
            name=row.stop_name,
            lat=row.stop_lat,
            lon=row.stop_lon
        )

        graph.add_station(station)

def _load_trips(
    graph: TransitGraph, 
    trips_file_name: str, 
    schedule_file_name: str, 
    exceptions_file_name: str, 
    routes_file_name: str) -> None: 
    
    # The data format in csv are little weird YYYYMMDD
    # Need to convert it to normal python date
    def convert_to_date(date_val) -> date:
        date_str = str(date_val)
        year = int(date_str[0:4])
        month = int(date_str[4:6])
        day = int(date_str[6:8])

        return date(year, month, day)

    # The dataframes
    trips_df = pd.read_csv(DATA_PATH + trips_file_name)
    trips_schedule_df = pd.read_csv(DATA_PATH + schedule_file_name).set_index('service_id')
    
    # Pre-index routes by route_id => faster look-up 
    routes_df = pd.read_csv(DATA_PATH + routes_file_name).set_index('route_id')
    
    # Pre-group exceptions by service_id so we don't rescan the whole dataframe
    schedule_exceptions_df = pd.read_csv(DATA_PATH + exceptions_file_name)
    exceptions_grouped = schedule_exceptions_df.groupby('service_id')

    for row in trips_df.itertuples():
        trip_id = row.trip_id
        service_id = row.service_id

        route_row = routes_df.loc[row.route_id]
        
        if (pd.isna(route_row['route_short_name'])):
            route_name = route_row['route_long_name']
        else:
            route_name = route_row['route_short_name']

        # Retrive data about the schedule
        if service_id in trips_schedule_df.index:
            schedule_row = trips_schedule_df.loc[service_id]
            start_date = convert_to_date(schedule_row['start_date'])
            end_date = convert_to_date(schedule_row['end_date'])
            weekdays = [
                bool(schedule_row['monday']),
                bool(schedule_row['tuesday']),
                bool(schedule_row['wednesday']),
                bool(schedule_row['thursday']),
                bool(schedule_row['friday']),
                bool(schedule_row['saturday']),
                bool(schedule_row['sunday'])
            ]
        else:
            # Case if service is only defined in calendar_dates.txt
            start_date = date.today()
            end_date = date.today()
            weekdays = [False] * 7
        
        added_days = set()
        removed_days = set()

        # Check for the exceptions 
        if service_id in exceptions_grouped.groups:
            service_exceptions = exceptions_grouped.get_group(service_id)
            for exception_row in service_exceptions.itertuples():
                # 1 means day has been added
                # 2 means day has been removed
                if exception_row.exception_type == 1:
                    added_days.add(
                        convert_to_date(exception_row.date)
                    )
                else:
                    removed_days.add(
                        convert_to_date(exception_row.date)
                    )

        graph.add_trip(
            Trip(
                trip_id=trip_id,
                route_name=route_name,
                start_date=start_date,
                finish_date=end_date,
                weekdays=weekdays,
                removed_days=removed_days,
                added_days=added_days
            )
        )

def _load_edges(
    graph: TransitGraph, 
    edges_file_name: str) -> None:
    
    # Time is stored as a HH::MM::SS
    # There can be hours after the midnight
    def _convert_time_to_minutes(time_val) -> int:
        time_str = str(time_val)

        hour, minutes, _ = time_str.split(':')

        return int(hour) * 60 + int(minutes)

    edges_df = pd.read_csv(DATA_PATH + edges_file_name).sort_values(by=['trip_id', 'stop_sequence'])

    # We need to check the previous stop
    # To know where we are going from and where we are going to 
    prev_row = None

    for row in edges_df.itertuples():
        # If we start a file or we are in the middle of a trip 
        if prev_row is not None and prev_row.trip_id == row.trip_id:
            start_stop_id = graph.stop_id_mapping.get(int(prev_row.stop_id))
            destination_stop_id = graph.stop_id_mapping.get(int(row.stop_id))
            
            trip_id = row.trip_id
            
            arrival_time = _convert_time_to_minutes(row.arrival_time)
            departure_time = _convert_time_to_minutes(prev_row.departure_time)

            graph.add_edge(
                Edge(
                    start_stop_id= start_stop_id,
                    destination_stop_id= destination_stop_id,
                    arrival_time= arrival_time,
                    departure_time= departure_time,
                    trip_id= trip_id
                )
            )

        prev_row = row

# OMG the legendary self documenting code :O
# the name is self explanatory 
def loadGraph() -> TransitGraph: 
    print('Loading a graph ...')
    start_graph = time.time()
    graph = TransitGraph()
    
    # These functions need to be called in a specific way
    # stations -> trips -> edges
    # Otherwise it will fail because we need to know the stations platforms
    # And map them to the parent station

    # Load stations
    print('  Loading station ...')
    start_time = time.time()
    _load_stations(graph, 'stops.csv')
    print(f'  Finished loading stations - took {round(time.time()-start_time,2)}s')

    # Load Trips
    print('  Loading trips ...')
    start_time = time.time()
    _load_trips(graph, 'trips.csv', 'calendar.csv', 'calendar_dates.csv', 'routes.csv')
    print(f'  Finished loading trips - took {round(time.time()-start_time,2)}s')

    # Load edges -> connections between stations
    print('  Loading connections ...')
    start_time = time.time()
    _load_edges(graph, 'stop_times.csv')
    print(f'  Finished loading connections - took {round(time.time()-start_time,2)}s')

    print(f'Finished loading a graph - took {round(time.time()-start_graph,2)}s')

    return graph

if __name__ == "__main__":
    loadGraph()