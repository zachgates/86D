from .. import GameObject, CardHand, CardTable


class CardPlayer(GameObject):

    def __init__(self):
        """
        Initialize the `CardPlayer` with an empty `CardHand` record and without
        an assigned table.
        """
        self.__hands: List[CardHand] = [] # Initialize in subclass
        self.__table = None # Reference to a CardPlayer's CardTable

    def __str__(self):
        return '%s(%s)' % (self.__class__.__name__, self.count)

    @property
    def table(self):
        """
        Property getter: Points to a `CardTable` assigned to the `CardPlayer`.
        """
        return self.__table

    @table.setter
    def table(self, table: CardTable):
        """
        Property setter: Sanitizes a `CardTable` assigned to the `CardPlayer`.
        """
        # Check if the CardPlayer has already been assigned to a table.
        if self.table and (table is not None):
            self.log.error('CardPlayer already has a CardTable')

        # Ensure table is either a CardTable or no table.
        if isinstance(table, CardTable) or (table is None):
            self.__table = table
        else:
            self.log.warning('table must be of type CardTable subclass')

    @property
    def hands(self):
        """
        Property getter: Points to the `CardHand`s of the `CardPlayer`.
        """
        return tuple(self.__hands)

    @hands.setter
    def hands(self, hands: list):
        """
        Property setter: Sanitizes `CardHand`s assigned to the `CardPlayer`.
        """
        # Ensure all hands are CardHands
        if all(isinstance(hand, CardHand) for hand in hands):
            for hand in hands:
                hand.player = self
                self.__hands.append(hand)
        else:
            self.log.warning('hands must be of type CardHand or subclass')

    def hand(self, hand_ord: int = 0):
        """
        Returns the indicated `CardHand`, by `hand_ord`.

        Keyword arguments:
        hand_ord -- An integer representing the index of a `CardHand`.
        """
        try:
            # Try to access the indicated CardHand.
            return self.hands[hand_ord]
        except IndexError:
            # No CardHand at index.
            return None

    @property
    def cards(self):
        """
        Property getter: Points to all `PlayingCard`s the `CardPlayer` holds.
        """
        return tuple(card for hand in self.hands for card in hand.cards)


__all__ = ['CardPlayer', 'CardHand']
