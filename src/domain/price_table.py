from dataclasses import dataclass


@dataclass
class PriceTable:
    price_table: dict

    def getPrice(self, price_type):
        return self.price_table[price_type]