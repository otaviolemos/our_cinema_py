from dataclasses import dataclass

DEFAULT_MAP = [ 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

@dataclass
class Room:
    name: str
    map: list

    def __init__(self, name, map=None):
        self.name = name
        if (map == None):
            self.map = DEFAULT_MAP
        else:
            self.map = map

    def capacity(self):
        seats = 0
        for row in self.map:
            seats += row
        return seats