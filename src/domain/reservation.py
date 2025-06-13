from dataclasses import dataclass
from domain.errors import SeatAlreadyReservedError
from domain.price_type import PriceType
from domain.session import Session


@dataclass
class Reservation:
    seat: tuple[int, int]
    session: Session
    price_type: PriceType

    def __init__(self, seat: str, session: Session, price_type: PriceType):
        self.seat = seat
        self.session = session
        self.price_type = price_type

        if not self.session.sessionRoom.reserve_seat(
seat):
            raise SeatAlreadyReservedError