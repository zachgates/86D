import random

from dataclasses import *
from typing import *

from .. import GameObject
from . import PlayingCard, CardSet, CardDeck


@dataclass(repr=False)
class CardShoe(CardSet):
    """
    A device used to hold multiple decks of cards typically 4, 6 or 8.
    Cards are dealt one at a time from the shoe.
    """

    _discards: List[PlayingCard] = field(default_factory=list)

    @property
    def decks(self):
        """
        Property getter: Returns a tuple of the `CardDeck`s in the `CardShoe`.
        """
        return tuple(set(card.deck for card in self.cards))

    @property
    def discards(self) -> tuple:
        """
        Property getter: Points to all discarded `PlayingCard`s.
        """
        return tuple(self._discards)

    def load(self, n_decks: int = 0) -> None:
        """
        Load the `CardShoe` with any number, N, `CardDeck`s.
        """
        for _ in range(n_decks):
            self._cards += CardDeck().cards

    def reload(self) -> None:
        """
        Move any discarded `PlayingCard`s back into the CardShoe.
        """
        self._cards.extend(self._discards)
        self._discards = []
        self.log.info('reloaded')

    def shuffle(self, n_repeat: int = 1) -> None:
        """
        Shuffle the `PlayingCard`s in the `CardShoe`. Repeat N times.

        Keyword arguments:
        n_repeat -- Integer representing the number of times, N, to shuffle.
        """
        for _ in range(n_repeat): # Repeat shuffle any, N, times.
            random.shuffle(self._cards)

    def draw(self) -> Optional[PlayingCard]:
        """
        Draw any number, N, `PlayingCard`s from the `CardShoe`.
        """
        if self.empty:
            self.log.warning('the CardShoe is empty')
        else:
            return self._cards.pop() # Draw a PlayingCard.

    def discard(self, card: PlayingCard) -> None:
        """
        Discard a `PlayingCard` handed to `CardDealer`.
        """
        self._discards.append(card)


__all__ = ['PlayingCard', 'CardDeck', 'CardShoe']
