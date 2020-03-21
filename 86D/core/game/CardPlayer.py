from dataclasses import field
from typing import List

from .. import gameclass, GameObject


@gameclass
class CardPlayer(GameObject):

    table: "CardTable" = None
    hands: List["CardHand"] = field(default_factory=list)
    funds: int = 0

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


__all__ = ['CardPlayer']
