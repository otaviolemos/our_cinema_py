class DuplicateRoomName(Exception):
    pass

class OverlappingSessionsOnSameRoom(Exception):
    pass

class SeatAlreadyReservedError(Exception):
    pass

class SeatDoesNotExistInSessionError(Exception):
    pass