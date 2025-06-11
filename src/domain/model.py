from dataclasses import dataclass, field
from enum import Enum
from src.domain.errors import DuplicateRoomName, OverlappingSessionsOnSameRoom, SeatAlreadyReservedError, SeatDoesNotExistInSessionError
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
DEFAULT_MAP = [ 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

@dataclass
class Room:
    name: str
    map: list

    def __init__(self, name, map=None):
        self.name = name
        if (map == None):
            self.map = DEFAULT_MAP
        else:
            self.map = map

    def capacity(self):
        seats = 0
        for row in self.map:
            seats += row
        return seats

@dataclass
class SessionRoom:
    room: Room
    rows: list[list[Seat]]

    def __init__(self, room):
        self.room = room
        self.rows = []
        row_code = ASCII_CODE_FOR_A
        for row in self.room.map:
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
    
    def available_seats(self):
        available_seats = 0
        for row in self.rows:
            for seat in row:
                if seat.is_available:
                    available_seats += 1
        return available_seats
    
    def reserve_seat(self, seat: str):
        indices = convert_seat_notation_to_indices(seat)

        if indices[0] >= len(self.rows) or indices[1] >= len(self.rows[indices[0]]):
            raise SeatDoesNotExistInSessionError

        return self.rows[indices[0]][indices[1]].reserve()
    
def convert_seat_notation_to_indices(seat_notation: str) -> tuple[int, int]:
    row_letter = seat_notation[0].upper()
    seat_number_str = seat_notation[1:]

    if not row_letter.isalpha():
        raise ValueError(f"Row must be a letter, got '{row_letter}'")

    try:
        seat_number = int(seat_number_str)
        if seat_number < 0:
            raise ValueError(f"Seat number must be positive.")
    except ValueError:
        raise ValueError(f"Invalid seat number: '{seat_number_str}'")

    row_index = ord(row_letter) - ord('A')
    column_index = seat_number - 1
    
    return (row_index, column_index)

    
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
    
@dataclass
class Theater:
    rooms: list[Room] = field(default_factory=list)
    sessions: list[Session] = field(default_factory=list)

    def add(self, room):
        if self.duplicate_room_name(room):
            raise DuplicateRoomName
        self.rooms.append(room)

    def remove(self, room):
        self.rooms.remove(room)

    def add_session(self, session):
        sessions_in_same_room = [theaterSession for theaterSession in self.sessions if theaterSession.sessionRoom.room == session.sessionRoom.room]
        for theaterSession in sessions_in_same_room:
            if (theaterSession.overlaps(session)):
                raise OverlappingSessionsOnSameRoom
        self.sessions.append(session)

    def remove_session(self, session):
        self.sessions.remove(session)

    def duplicate_room_name(self, room):
        return [theater_room for theater_room in self.rooms if theater_room.name == room.name]
    
class PriceType(Enum):
    SENIOR = "senior"
    REGULAR = "regular"
    STUDENT_HALF = "student_half"

@dataclass
class Reservation:
    seat: tuple[int, int]
    session: Session
    price_type: PriceType

    def __init__(self, seat: str, session: Session, price_type: PriceType):
        self.seat = seat
        self.session = session
        self.price_type = price_type

        if not self.session.sessionRoom.reserve_seat(seat):
            raise SeatAlreadyReservedError
        
@dataclass
class PriceTable:
    price_table: dict

    def getPrice(self, price_type):
        return self.price_table[price_type]

@dataclass
class User:
    username: str

@dataclass
class ShoppingCart:
    user: User
    reservations: list[Reservation]
    price_table: PriceTable

    def total_price(self):
        total = 0.0
        for reservation in self.reservations:
            total += self.price_table.getPrice(reservation.price_type)
        return total