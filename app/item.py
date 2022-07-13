from random import choice

class Size:
    SMALL = 'small'
    BIG = 'big'

class Item:

    def __init__(self, height: float, width: float, length: float, fragile: bool):
        self.height = height
        self.width = width
        self.length = length
        self.fragile = fragile

    @property
    def size(self):
        height = max(self.height, 1)
        width = max(self.width, 1)
        length = max(self.length, 1)

        dimensions_sum = height + width + length

        if 0 < dimensions_sum < 30:
            return Size.SMALL
        else:
            return Size.BIG

    @classmethod
    def random(cls, fragile: bool = False, size: str = Size.BIG):
        if size == Size.SMALL:
            return cls(
                height=choice(range(1, 10)),
                width=choice(range(1, 10)),
                length=choice(range(1, 10)),
                fragile=fragile
            )
        elif size == Size.BIG:
            return cls(
                height=choice(range(10, 1000)),
                width=choice(range(10, 1000)),
                length=choice(range(10, 1000)),
                fragile=fragile
            )
