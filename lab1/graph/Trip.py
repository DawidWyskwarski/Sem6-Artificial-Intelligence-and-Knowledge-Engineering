from dataclasses import dataclass
from datetime import date
from typing import List

@dataclass
class Trip:
    trip_id: int
    route_name: str
    start_date: date
    finish_date: date
    weekdays: List[bool]
    removed_days: set[date]
    added_days: set[date]

    def is_active(self, date: date) -> bool:
        if date in self.removed_days:
            return False
        
        if date in self.added_days:
            return True
        
        if self.start_date <= date <= self.finish_date and self.weekdays[date.weekday()]:
            return True

        return False 