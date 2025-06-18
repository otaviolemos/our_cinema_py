from uuid import uuid4
from domain.reservation import Reservation


class FakeReservationRepository:
    """An in-memory implementation of the ReservationRepository protocol for testing"""
    
    def __init__(self, initial_reservations: list[Reservation] = None):
        for reservation in initial_reservations or []:
            if reservation.id is None:
                reservation.id = uuid4()
        self.reservations = initial_reservations or []

    def save(self, reservation: Reservation) -> None:
        """Save a reservation to the repository.
        If the reservation already exists, it will be updated."""
        if reservation.id is None:
            reservation.id = uuid4()
        
        for i, existing_reservation in enumerate(self.reservations):
            if existing_reservation.id == reservation.id:
                self.reservations[i] = reservation
                return
        self.reservations.append(reservation)