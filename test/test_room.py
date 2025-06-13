from domain.room import Room
from domain.session_room import SessionRoom

def test_create_session_room():
    room = Room("1")
    sessionRoom = SessionRoom(room)
    assert len(sessionRoom.rows) == 10
    assert len(sessionRoom.rows[5]) == 10
    first_seat = sessionRoom.rows[0][0]
    assert first_seat.row == "A"
    assert first_seat.number == 1

def test_create_room_with_custom_map():
    map = [10, 10, 10, 20, 20, 10, 10]
    room = Room("1", map)
    sessionRoom = SessionRoom(room)
    assert len(sessionRoom.rows[3]) == 20

def test_capacity_for_default_map():
    room = Room("1")
    assert room.capacity() == 100

def test_get_available_seats():
    room = Room("1")
    sessionRoom = SessionRoom(room)
    assert sessionRoom.available_seats() == 100