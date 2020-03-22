from .. import GameObject


class CasinoToken(GameObject):
    """
    A dataclass representing a single CasinoToken of a denomination.
    """

    TokenColors = ['white', 'yellow', 'red', 'blue', 'grey', 'green', 'orange', 'black']
    TokenValues = [1, 2, 5, 10, 20, 25, 50, 100]

    value: int

    def __post_init__(self):
        """
        Verify the `CasinoToken`'s value.
        """
        self._assert((self.value in self.TokenValues), 'no $%i chip.' % self.value)

    def __eq__(self, other):
        self._assert(isinstance(other, CasinoToken), 'cannot compare non-token.')
        return self.value == other.value

    def __str__(self):
        """
        Render a `CasinoToken` to a human-readable string.
        """
        return 'Chip($%i)' % self.value

    @property
    def color(self):
        """
        Property getter: Returns the color of this denomination of CasinoToken.
        """
        return self.TokenColors[self.value]


__all__ = ['CasinoToken']
