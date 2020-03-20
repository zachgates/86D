from dataclasses import *

from .. import gameclass, GameObject


@gameclass
class CasinoToken(GameObject):
    """
    A dataclass representing a single CasinoToken of a denomination.
    """

    TokenColors = ['white', 'yellow', 'red', 'blue', 'grey', 'green', 'orange', 'black']
    TokenValues = [1, 2, 5, 10, 20, 25, 50, 100]

    value: int

    def __post_init__(self):
        self._assert((self.value in self.TokenValues), 'no $%i chip.' % self.value)

    def __str__(self):
        return 'Chip($%i)' % self.value

    @property
    def color(self):
        """
        Property getter: Returns the color of this denomination of CasinoToken.
        """
        return self.TokenColors[self.value]
