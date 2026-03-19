from dataclasses import dataclass

# The node of the graph
# In TransitGraph we have dictionaty where we connect Stations with edges
@dataclass
class Station:
    station_id: int
    # For human readability
    name: str
    # Lat and lon can be used as a heuristic
    lat: float
    lon: float