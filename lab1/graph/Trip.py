from dataclasses import dataclass
from typing import List
from datetime import date

# The Edge has reference to the trip_id
# This class has all of the necessary info to determine wether an Edge is active or not
# I think it would be weird to store these informations in the Edge
# Does it make the code more complex ? Yes
# Maybe place for improvement
@dataclass
class Trip:
    trip_id: int
    route_name: str
    start_date: date
    finish_date: date
    weekdays: List[bool]
    removed_days: List[date]
    added_days: List[date]

