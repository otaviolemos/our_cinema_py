from dataclasses import dataclass
from datetime import timedelta
from typing import Optional
from uuid import UUID


@dataclass
class Movie:
    title: str
    genre: str
    duration: int
    id: Optional[UUID] = None

    def formatted_duration(self):
        hours = self.duration // 60
        minutes = self.duration % 60
        if minutes > 0 and hours > 0:
            return f"{hours}h{minutes}min"
        elif hours > 0:
            return f"{hours}h"
        else:
            return f"{minutes}min"
        
    def get_duration_as_timedelta(self):
        return timedelta(minutes=self.duration)