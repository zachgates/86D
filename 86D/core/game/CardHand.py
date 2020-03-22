from typing import List

from .. import CardSet
from . import CardPlayer


class CardHand(CardSet):
    """
    A dataclass representing a single `CardHand` of `PlayingCard`s.
    """

    player: CardPlayer
    bet: int = 0

    def add(self, card: "PlayingCard"):
        """
        Add a `PlayingCard` to the `CardHand`.
        """
        super().add(card)
        card.hand = self # Reference this CardHand from the PlayingCard.

    def discard(self, card: "PlayingCard" = None):
        """
        Discard either a single `PlayingCard` from the `CardHand`, or all
        `PlayingCard`s from the `CardHand`, if supplied `card is None`.
        """
        if card:
            super().discard(card)
            card.hand = None # Unassign a CardHand.
        else:
            # Discard all PlayingCards from the CardHand.
            self.player.table.dealer.discard(cards=self.cards)
            self.log.debug('discarded.')


__all__ = ['CardHand']
