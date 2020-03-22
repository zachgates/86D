from typing import List

from .. import gameclass, GameObject
from . import PlayingCard


@gameclass
class CardSet(GameObject):
    """
    A dataclass representing any collection of `PlayingCard`s.
    """

    cards: List[PlayingCard]

    def __eq__(self, other):
        return set(self.cards) == set(other.cards)

    def __str__(self):
        """
        Render a `CardSet` to a human-readable string.
        """
        str_ = str(tuple(str(card) for card in self.cards))
        str_ = str_.replace("'", '')
        return str_

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
        self.log.debug('turned face-up.')

    def add(self, card: PlayingCard) -> None:
        """
        Add a `PlayingCard` to the `CardSet`.
        """
        self._assert(isinstance(card, PlayingCard), 'card not a PlayingCard.')
        self.cards.append(card)
        self.log.debug('add(%r)' % card)

    def discard(self, card: PlayingCard) -> None:
        """
        Discard a single `PlayingCard` from the `CardSet`.
        """
        # Inspect the supplied card.
        self._assert((card in self.cards), 'supplied card not in CardSet.')
        # Discard the supplied PlayingCard from the CardSet.
        self.cards.remove(card)
        self.log.debug('discard(%r)' % card)


__all__ = ['CardSet']
