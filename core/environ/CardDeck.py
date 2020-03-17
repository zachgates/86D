from dataclasses import *
from typing import *

from .. import GameObject
from . import PlayingCard


@dataclass
class CardDeck(GameObject):
    """
    A dataclass representing an entire `CardDeck` of `PlayingCard`s.
    """

    def deck_factory():
        """
        Creates all fifty-two (52) `PlayingCard`s in the `CardDeck`. The
        reference to a CardDeck is assigned in post-init.
        """
        return [PlayingCard(rank, suit) \
                for rank in PlayingCard.RANK_ORDS \
                for suit in PlayingCard.SUIT_ORDS]

    cards: List[PlayingCard] = field(default_factory=deck_factory)

    def __post_init__(self):
        """
        Post-initialize a reference to this `CardDeck` on each `PlayingCard`.
        """
        for card in self.cards:
            card.deck = self
        self.log.debug('generated (52) cards')

    @property
    def empty(self):
        """
        Property getter: Points to whether the `CardDeck` contains any
        `PlayingCard`s.
        """
        return len(self.cards) == 0


__all__ = ['CardDeck', 'PlayingCard']
