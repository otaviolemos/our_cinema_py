from dataclasses import dataclass, field
from enum import Enum
from src.domain.errors import DuplicateRoomName
from datetime import datetime, timedelta

class SeatStatus(Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    OCCUPIED = "occupied"

@dataclass
class Seat:
    row: str
    number: int
    status: SeatStatus = SeatStatus.AVAILABLE

    @property
    def is_available(self):
        return self.status == SeatStatus.AVAILABLE
    
    def reserve(self):
        if self.status == SeatStatus.AVAILABLE:
            self.status = SeatStatus.RESERVED
            return True
        return False
    
    def confirm(self):
        if self.status == SeatStatus.RESERVED:
            self.status = SeatStatus.OCCUPIED
            return True
        return False
    
    def release(self):
        self.status = SeatStatus.AVAILABLE

    
ASCII_CODE_FOR_A = 65

@dataclass
class Room:
    name: str
    rows: list[list[Seat]]

    def __init__(self, name, seats=None):
        self.name = name
        self.rows = []
        if seats is None:
            self.create_list_of_seats()
            return
        row_code = ASCII_CODE_FOR_A
        for row in seats:
            row_seats = []
            row_name = chr(row_code)
            for j in range(row):
                seat = Seat(row=row_name, number=j+1)
                row_seats.append(seat)
            self.rows.append(row_seats)
            row_code += 1

    def create_list_of_seats(self):
        for i in range(10):
            row = chr(i + 65)
            row_seats = []
            for j in range(10):
                seat = Seat(row=row, number=j+1)
                row_seats.append(seat)
            self.rows.append(row_seats)

    def capacity(self):
        seats = 0
        for row in self.rows:
            seats += len(row)
        return seats
    
    def available_seats(self):
        available_seats = 0
        for row in self.rows:
            for seat in row:
                if seat.is_available:
                    available_seats += 1
        return available_seats
    
@dataclass
class Theater:
    rooms: list[Room] = field(default_factory=list)

    def add(self, room):
        if self.duplicate_room_name(room):
            raise DuplicateRoomName
        self.rooms.append(room)

    def remove(self, room):
        self.rooms.remove(room)

    def duplicate_room_name(self, room):
        return [theater_room for theater_room in self.rooms if theater_room.name == room.name]
    
@dataclass
class Movie:
    title: str
    genre: str
    duration: int

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
        
@dataclass
class Session:
    room: Room
    movie: Movie
    start_time: datetime

    def end_time(self):
        return self.start_time + self.movie.get_duration_as_timedelta()