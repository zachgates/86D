from dataclasses import *
from typing import *

from .. import gameclass, GameObject
from . import CardHand


@gameclass
class CardPlayer(GameObject):

    _table: "CardTable" = None
    _hands: List[CardHand] = field(default_factory=list)
    _funds: int = 0

    @property
    def table(self):
        """
        Property getter: Points to a `CardTable` assigned to the `CardPlayer`.
        """
        return self._table

    @table.setter
    def table(self, table: "CardTable"):
        """
        Property setter: Sanitizes a `CardTable` assigned to the `CardPlayer`.
        """
        from . import CardTable # Avoid circular import.
        # Check if the CardPlayer has already been assigned to a table.
        if table:
            self._assert(not self.table, 'CardPlayer already has a CardTable.')
            return
        # Ensure table is either a CardTable or no table.
        self._assert(isinstance(table, (CardTable, type(None))),
                    'table must be CardTable or subclass, or None.')
        self._table = table

    @property
    def hands(self):
        """
        Property getter: Points to the `CardHand`s of the `CardPlayer`.
        """
        return tuple(self._hands)

    @hands.setter
    def hands(self, hands: list):
        """
        Property setter: Sanitizes `CardHand`s assigned to the `CardPlayer`.
        """
        # Ensure all hands are CardHands.
        self._assert(all(isinstance(hand, CardHand) for hand in hands),
                    'all hands must be of type CardHand or subclass.')
        # Assign each CardHand to the CardPlayer.
        for hand in hands:
            hand.player = self
            self._hands.append(hand)

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
            self._assert(False, 'no CardHand at index: %i.' % hand_ord)
            return None

    @property
    def cards(self):
        """
        Property getter: Points to all `PlayingCard`s the `CardPlayer` holds.
        """
        return tuple(card for hand in self.hands for card in hand.cards)

    @property
    def funds(self):
        """
        Property getter: Points to the total value of the `CardPlayer`'s funds.
        """
        return self._funds


__all__ = ['CardPlayer']
