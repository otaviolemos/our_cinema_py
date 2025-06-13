from dataclasses import dataclass
from datetime import datetime

from domain.movie import Movie
from domain.session_room import SessionRoom


@dataclass
class Session:
    sessionRoom: SessionRoom
    movie: Movie
    start_time: datetime

    def __init__(self, room, movie, start_time):
        self.movie = movie
        self.sessionRoom = SessionRoom(room)
        self.start_time = start_time

    @property
    def end_time(self):
        return self.start_time + self.movie.get_duration_as_timedelta()
    
    def available_seats(self):
        return self.sessionRoom.available_seats()
    
    def overlaps(self, session):
        if self.start_time < session.end_time and self.end_time > session.start_time:
            return True
        return False