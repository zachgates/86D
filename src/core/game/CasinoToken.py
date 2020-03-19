from dataclasses import *

from .. import GameObject


@dataclass(repr=False)
class CasinoToken(GameObject):
    """
    A dataclass representing a single CasinoToken of a denomination.
    """

    COLORS = ['white', 'yellow', 'red', 'blue', 'grey', 'green', 'orange', 'black']
    VALUES = [1, 2, 5, 10, 20, 25, 50, 100]

    value: int

    @property
    def color(self):
        """
        Property getter: Returns the color of this denomination of CasinoToken.
        """
        return self.COLORS[self.value]
