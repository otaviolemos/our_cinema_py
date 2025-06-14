from typing import Protocol

from domain.user import User


class ReservationRepository(Protocol):
    def save(self, user: User) -> None: ...