from dataclasses import dataclass

from domain.errors import SeatDoesNotExistInSessionError
from domain.room import Room
from domain.seat import Seat
from domain.utils import convert_seat_notation_to_indices


ASCII_CODE_FOR_A = 65

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