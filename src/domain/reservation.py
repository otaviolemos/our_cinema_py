from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from domain.errors import SeatAlreadyReservedError
from domain.price_type import PriceType
from domain.session import Session
from domain.user import User


@dataclass
class Reservation:
    seats: list[tuple[int, int]]
    session: Session
    user: User
    price_types: list[PriceType]
    id: Optional[UUID] = None

    def __init__(self, seats: list[str], session: Session, user: User):
        self.seats = seats
        self.session = session
        self.price_type = []
        self.user = user

        for seat in seats:
            if not self.session.sessionRoom.is_available(seat):
                raise SeatAlreadyReservedError
            
        for seat in seats:
            self.session.sessionRoom.reserve_seat(seat)