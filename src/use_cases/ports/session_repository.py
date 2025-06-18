from typing import Protocol

from domain.reservation import Reservation


class SessionRepository(Protocol):
    def save(self, reservation: Reservation) -> None: ...