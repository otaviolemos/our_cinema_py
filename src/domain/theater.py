from dataclasses import dataclass, field

from domain.errors import DuplicateRoomName, OverlappingSessionsOnSameRoom
from domain.room import Room
from domain.session import Session


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