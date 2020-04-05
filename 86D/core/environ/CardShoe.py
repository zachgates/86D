import random

from dataclasses import field
from typing import List, Optional

from .. import GameObject
from . import CardSet, CardDeck


class CardShoe(CardSet):
    """
    A device used to hold multiple decks of cards typically 4, 6 or 8.
    Cards are dealt one at a time from the shoe.
    """

    cards: List["PlayingCard"] = field(default_factory=list)
    discards: List["PlayingCard"] = field(default_factory=list)

    def load(self, n_decks: int = 0) -> None:
        """
        Load the `CardShoe` with any number, N, `CardDeck`s.
        """
        self.log.debug('load(n_decks=%i)' % n_decks)
        for _ in range(n_decks):
            self.cards += CardDeck().cards

    def reload(self) -> None:
        """
        Move any discarded `PlayingCard`s back into the CardShoe.
        """
        self.cards.extend(self.discards)
        self.discards = []
        self.log.debug('reloaded.')

    def shuffle(self, n_repeat: int = 1) -> None:
        """
        Shuffle the `PlayingCard`s in the `CardShoe`. Repeat N times.

        Keyword arguments:
        n_repeat -- Integer representing the number of times, N, to shuffle.
        """
        for _ in range(n_repeat): # Repeat shuffle any, N, times.
            random.shuffle(self.cards)

    def draw(self) -> Optional["PlayingCard"]:
        if self.empty:
            self._assert(False, 'the CardShoe is empty.', warn=True)
            return None
        else:
            return self.cards.pop() # Draw a PlayingCard.

    def discard(self, card: "PlayingCard") -> None:
        """
        Discard a `PlayingCard` handed to `CardDealer`.
        """
        self.discards.append(card)


__all__ = ['CardShoe']
