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

# Layout rendering

def test_basic_10_x_10_layout():
    room = Room("1")
    sessionRoom = SessionRoom(room)

    layout = sessionRoom.ascLayout()

    expectedLayout = """
               [SCREEN]
A01 A02 A03 A04 A05 A06 A07 A08 A09 A10
B01 B02 B03 B04 B05 B06 B07 B08 B09 B10
C01 C02 C03 C04 C05 C06 C07 C08 C09 C10
D01 D02 D03 D04 D05 D06 D07 D08 D09 D10
E01 E02 E03 E04 E05 E06 E07 E08 E09 E10
F01 F02 F03 F04 F05 F06 F07 F08 F09 F10
G01 G02 G03 G04 G05 G06 G07 G08 G09 G10
H01 H02 H03 H04 H05 H06 H07 H08 H09 H10
I01 I02 I03 I04 I05 I06 I07 I08 I09 I10
J01 J02 J03 J04 J05 J06 J07 J08 J09 J10
"""

    assert layout == expectedLayout

def test_basic_layout_with_reserved_seats():
    room = Room("1")
    sessionRoom = SessionRoom(room)
    sessionRoom.reserve_seat("D5")
    sessionRoom.reserve_seat("I10")

    layout = sessionRoom.ascLayout()

    expectedLayout = """
               [SCREEN]
A01 A02 A03 A04 A05 A06 A07 A08 A09 A10
B01 B02 B03 B04 B05 B06 B07 B08 B09 B10
C01 C02 C03 C04 C05 C06 C07 C08 C09 C10
D01 D02 D03 D04 XXX D06 D07 D08 D09 D10
E01 E02 E03 E04 E05 E06 E07 E08 E09 E10
F01 F02 F03 F04 F05 F06 F07 F08 F09 F10
G01 G02 G03 G04 G05 G06 G07 G08 G09 G10
H01 H02 H03 H04 H05 H06 H07 H08 H09 H10
I01 I02 I03 I04 I05 I06 I07 I08 I09 XXX
J01 J02 J03 J04 J05 J06 J07 J08 J09 J10
"""
    assert layout == expectedLayout

def test_custom_layout():
    room = Room("1", [8, 9, 10, 10, 10, 10, 10, 10, 9, 8])
    sessionRoom = SessionRoom(room)

    layout = sessionRoom.ascLayout()

    expectedLayout = """
               [SCREEN]
    A01 A02 A03 A04 A05 A06 A07 A08
  B01 B02 B03 B04 B05 B06 B07 B08 B09
C01 C02 C03 C04 C05 C06 C07 C08 C09 C10
D01 D02 D03 D04 D05 D06 D07 D08 D09 D10
E01 E02 E03 E04 E05 E06 E07 E08 E09 E10
F01 F02 F03 F04 F05 F06 F07 F08 F09 F10
G01 G02 G03 G04 G05 G06 G07 G08 G09 G10
H01 H02 H03 H04 H05 H06 H07 H08 H09 H10
  I01 I02 I03 I04 I05 I06 I07 I08 I09
    J01 J02 J03 J04 J05 J06 J07 J08
"""
    assert layout == expectedLayout