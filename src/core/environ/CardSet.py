from dataclasses import *
from typing import *

from .. import GameObject
from . import PlayingCard


@dataclass
class CardSet(GameObject):
    """
    A dataclass representing any collection of `PlayingCard`s.
    """

    _cards: List[PlayingCard] = field(default_factory=list)

    def __hash__(self):
        return hash((self.__class__, self.count))

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
