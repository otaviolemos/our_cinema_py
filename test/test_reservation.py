from datetime import datetime, timedelta
from domain.room import Room
from domain.price_type import PriceType
from domain.reservation import Reservation
from domain.session import Session
from domain.errors import SeatAlreadyReservedError, SeatDoesNotExistInSessionError
from domain.utils import convert_seat_notation_to_indices
from test.builder.movie_builder import MovieBuilder
import pytest

def test_create_valid_reservation():
    room = Room("1")
    movie = MovieBuilder().aMovie().with_duration(90).build()
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow_at_seven_pm = tomorrow.replace(hour=19, minute=0, second=0, microsecond=0)
    session = Session(room=room, movie=movie, start_time=tomorrow_at_seven_pm)

    Reservation(seat='A1', session=session, price_type=PriceType.SENIOR)
    Reservation(seat='J10', session=session, price_type=PriceType.REGULAR)

    assert not session.sessionRoom.rows[0][0].is_available
    assert not session.sessionRoom.rows[9][9].is_available

def test_create_reservation_for_reserved_seat():
    room = Room("1")
    movie = MovieBuilder().aMovie().with_duration(90).build()
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow_at_seven_pm = tomorrow.replace(hour=19, minute=0, second=0, microsecond=0)
    session = Session(room=room, movie=movie, start_time=tomorrow_at_seven_pm)

    Reservation(seat='A1', session=session, price_type=PriceType.SENIOR)
    with pytest.raises(SeatAlreadyReservedError):
        Reservation(seat='A1', session=session, price_type=PriceType.SENIOR)

def test_reservation_for_non_existing_session_seat_row():
    room = Room("1")
    movie = MovieBuilder().aMovie().with_duration(90).build()
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow_at_seven_pm = tomorrow.replace(hour=19, minute=0, second=0, microsecond=0)
    session = Session(room=room, movie=movie, start_time=tomorrow_at_seven_pm)

    with pytest.raises(SeatDoesNotExistInSessionError):
        Reservation(seat='K1', session=session, price_type=PriceType.SENIOR)

def test_reservation_for_non_existing_session_seat():
    room = Room("1")
    movie = MovieBuilder().aMovie().with_duration(90).build()
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow_at_seven_pm = tomorrow.replace(hour=19, minute=0, second=0, microsecond=0)
    session = Session(room=room, movie=movie, start_time=tomorrow_at_seven_pm)

    with pytest.raises(SeatDoesNotExistInSessionError):
        Reservation(seat='A11', session=session, price_type=PriceType.SENIOR)


def test_seat_notation_without_first_letter():
    with pytest.raises(ValueError):
        convert_seat_notation_to_indices('99')

def test_seat_notation_without_row_number():
    with pytest.raises(ValueError):
        convert_seat_notation_to_indices('AA')

def test_seat_notation_negative_row_number():
    with pytest.raises(ValueError):
        convert_seat_notation_to_indices('A-1')