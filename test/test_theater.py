from datetime import datetime, timedelta
from domain.room import Room
from domain.session import Session
from domain.theater import Theater
from domain.errors import DuplicateRoomName, OverlappingSessionsOnSameRoom
import pytest
from test.builder.movie_builder import MovieBuilder

def test_can_add_room_to_theater():
    theater = Theater()
    room1 = Room("1")
    theater.add(room1)
    assert room1 in theater.rooms

def test_can_remove_room_from_theater():
    theater = Theater()
    room1 = Room("1")
    theater.add(room1)
    theater.remove(room1)
    assert room1 not in theater.rooms

def test_theater_room_has_unique_name():
    theater = Theater()
    room1 = Room("1")
    room2 = Room("1")
    theater.add(room1)
    with pytest.raises(DuplicateRoomName):
        theater.add(room2)

def test_can_add_session_to_theater():
    theater = Theater()
    room = Room("1")
    theater.add(room)
    movie = MovieBuilder().aMovie().with_duration(90).build()
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow_at_seven_pm = tomorrow.replace(hour=19, minute=0, second=0, microsecond=0)
    session = Session(room=room, movie=movie, start_time=tomorrow_at_seven_pm)
    theater.add_session(session)
    assert session in theater.sessions

def test_can_remove_session_from_theater():
    theater = Theater()
    room = Room("1")
    theater.add(room)
    movie = MovieBuilder().aMovie().with_duration(90).build()
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow_at_seven_pm = tomorrow.replace(hour=19, minute=0, second=0, microsecond=0)
    session = Session(room=room, movie=movie, start_time=tomorrow_at_seven_pm)
    theater.add_session(session)
    theater.remove_session(session)
    assert session not in theater.sessions 

def test_sessions_overlap_on_same_room():
    theater = Theater()
    room = Room("1")
    theater.add(room)
    movie = MovieBuilder().aMovie().with_duration(90).build()
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow_at_seven_pm = tomorrow.replace(hour=19, minute=0, second=0, microsecond=0)
    session1 = Session(room=room, movie=movie, start_time=tomorrow_at_seven_pm)
    theater.add_session(session1)
    tomorrow_at_eigh_pm = tomorrow.replace(hour=20, minute=0, second=0, microsecond=0)
    session2 = Session(room=room, movie=movie, start_time=tomorrow_at_eigh_pm)
    with pytest.raises(OverlappingSessionsOnSameRoom):
        theater.add_session(session2)