from domain.reservation import Reservation


class FakeReservationRepository:
    """An in-memory implementation of the ReservationRepository protocol for testing"""
    
    def __init__(self, initial_reservations: list[Reservation] = None):
        self.reservations = initial_reservations or []