from datetime import datetime, timedelta
from domain.room import Room
from domain.price_type import PriceType
from domain.reservation import Reservation
from domain.session import Session
from domain.errors import SeatAlreadyReservedError, SeatDoesNotExistInSessionError
from domain.user import User
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
    user = User('test_user')

    Reservation(seats=['A1', 'J10'], session=session, user=user)

    assert not session.sessionRoom.rows[0][0].available
    assert not session.sessionRoom.rows[9][9].available

def test_create_reservation_for_reserved_seat():
    room = Room("1")
    movie = MovieBuilder().aMovie().with_duration(90).build()
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow_at_seven_pm = tomorrow.replace(hour=19, minute=0, second=0, microsecond=0)
    session = Session(room=room, movie=movie, start_time=tomorrow_at_seven_pm)
    user = User('test_user')

    Reservation(seats=['A1'], session=session, user=user)
    with pytest.raises(SeatAlreadyReservedError):
        Reservation(seats=['A1'], session=session, user=user)

def test_create_reservation_for_valid_and_reserved_seat():
    room = Room("1")
    movie = MovieBuilder().aMovie().with_duration(90).build()
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow_at_seven_pm = tomorrow.replace(hour=19, minute=0, second=0, microsecond=0)
    session = Session(room=room, movie=movie, start_time=tomorrow_at_seven_pm)
    user = User('test_user')

    Reservation(seats=['A2'], session=session, user=user)
    with pytest.raises(SeatAlreadyReservedError):
        Reservation(seats=['A1', 'A2'], session=session, user=user)
    assert session.sessionRoom.is_available('A10')

def test_reservation_for_non_existing_session_seat_row():
    room = Room("1")
    movie = MovieBuilder().aMovie().with_duration(90).build()
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow_at_seven_pm = tomorrow.replace(hour=19, minute=0, second=0, microsecond=0)
    session = Session(room=room, movie=movie, start_time=tomorrow_at_seven_pm)
    user = User('test_user')

    with pytest.raises(SeatDoesNotExistInSessionError):
        Reservation(seats=['K1'], session=session, user=user)

def test_reservation_for_non_existing_session_seat():
    room = Room("1")
    movie = MovieBuilder().aMovie().with_duration(90).build()
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow_at_seven_pm = tomorrow.replace(hour=19, minute=0, second=0, microsecond=0)
    session = Session(room=room, movie=movie, start_time=tomorrow_at_seven_pm)
    user = User('test_user')

    with pytest.raises(SeatDoesNotExistInSessionError):
        Reservation(seats=['A11'], session=session, user=user)