from dataclasses import dataclass

from domain.reservation import Reservation
from domain.price_table import PriceTable
from domain.user import User


@dataclass
class ShoppingCart:
    user: User
    reservations: list[Reservation]
    price_table: PriceTable

    def total_price(self):
        total = 0.0
        for reservation in self.reservations:
            total += self.price_table.getPrice(reservation.price_type)
        return total