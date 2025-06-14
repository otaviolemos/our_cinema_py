from typing import Protocol

from domain.reservation import Reservation


class ReservationRepository(Protocol):
    def save(self, reservation: Reservation) -> None: ...
    def find_for_session(self, session_id: str) -> list[Reservation]: ...