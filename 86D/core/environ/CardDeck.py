from dataclasses import field
from typing import List

from .. import gameclass
from . import PlayingCard, CardSet


@gameclass
class CardDeck(CardSet):
    """
    A dataclass representing an entire `CardDeck` of `PlayingCard`s.
    """

    def deck_factory():
        """
        Creates all fifty-two (52) `PlayingCard`s in the `CardDeck`. The
        reference to a CardDeck is assigned in post-init.
        """
        return [PlayingCard(rank, suit) \
                for rank in PlayingCard.RankRange \
                for suit in PlayingCard.SuitRange]

    cards: List[PlayingCard] = field(default_factory=deck_factory)

    def __post_init__(self):
        """
        Post-initialize a reference to this `CardDeck` on each `PlayingCard`.
        """
        for card in self.cards:
            card.deck = self
        self.log.debug('generated (52) cards.')


__all__ = ['CardDeck']
