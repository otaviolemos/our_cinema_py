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
                if seat.available:
                    available_seats += 1
        return available_seats
    
    def reserve_seat(self, seat: str):
        indices = convert_seat_notation_to_indices(seat)

        if indices[0] >= len(self.rows) or indices[1] >= len(self.rows[indices[0]]):
            raise SeatDoesNotExistInSessionError

        return self.rows[indices[0]][indices[1]].reserve()
    
    def is_available(self, seat: str):
        indices = convert_seat_notation_to_indices(seat)

        if indices[0] >= len(self.rows) or indices[1] >= len(self.rows[indices[0]]):
            raise SeatDoesNotExistInSessionError

        return self.rows[indices[0]][indices[1]].available

    def ascLayout(self):
        layout = "\n"

        lenLargestRow = -1
        for row in self.rows:
            lenRow = len(row)
            if lenRow > lenLargestRow:
                lenLargestRow = lenRow
        
        lenLargestRow = (lenLargestRow * 4) - 1

        print("Len largest row " + str(lenLargestRow))
        
        screenLabel = "[SCREEN]"
        lenScreen = len(screenLabel)
        diff = lenLargestRow - lenScreen

        layout = layout + (int(diff / 2) * ' ') + screenLabel
        layout += '\n'

        row_code = ASCII_CODE_FOR_A
        for row in self.rows:
            row_name = chr(row_code)
            lenRow = len(row)
            diff = lenLargestRow - ((lenRow * 4) - 1)
            layout = layout + (int(diff / 2) * ' ')
            for j in range(lenRow):
                if (row[j].available):
                    seat_name = row_name
                    seat_number = j+1
                    if seat_number < 10:
                        seat_name += "0"
                    seat_name += str(seat_number)
                else:
                    seat_name = "XXX"
                layout += seat_name + " "
            layout = layout.rstrip()
            row_code += 1
            layout += "\n"

        return layout