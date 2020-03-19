from dataclasses import *
from typing import *

from .. import GameObject
from . import PlayingCard


@dataclass(repr=False)
class CardSet(GameObject):
    """
    A dataclass representing any collection of `PlayingCard`s.
    """

    _cards: List[PlayingCard] = field(default_factory=list)

    @property
    def cards(self):
        """
        Property getter: Returns a `tuple` containing all `PlayingCard`s.
        """
        return tuple(self._cards)

    @property
    def empty(self):
        """
        Property getter: Points to whether the `CardDeck` contains any
        `PlayingCard`s.
        """
        return len(self.cards) == 0

    @property
    def up(self) -> bool:
        """
        Property getter: Points to whether all `PlayingCard`s are face-up.
        """
        return all(card.up for card in self.cards)

    @up.setter
    def up(self, reveal: bool):
        """
        Property setter: Apply `PlayingCard` orientation changes.
        """
        for card in self.cards:
            card.up = bool(reveal)
        self.log.debug('turned face-up')

    def add(self, card: PlayingCard) -> None:
        """
        Add a `PlayingCard` to the `CardHand`.
        """
        assert isinstance(card, PlayingCard), 'supplied card not a PlayingCard'
        self._cards.append(card)
        card.hand = self # Reference this CardHand from the PlayingCard.
        self.log.debug('add->%r' % card)

    def discard(self, card: PlayingCard = None) -> None:
        """
        Discard either a single `PlayingCard` from the `CardHand`, or all
        `PlayingCard`s from the `CardHand`, if supplied `card is None`.
        """
        if card:
            # Inspect the supplied card.
            if card not in self.cards:
                self.log.error('supplied card not in CardHand')
            # Discard the supplied PlayingCard from the CardHand.
            card.hand = None # Unassign a CardHand.
            self._cards.remove(card)
            self.log.debug('discard->%r' % card)
        else:
            # Discard all PlayingCards from the CardHand.
            for card in self.cards:
                card.discard()
            self.log.debug('discarded')
