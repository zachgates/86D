import random

from typing import *

from .. import GameObject
from . import PlayingCard, CardDeck


class CardShoe(GameObject):
    """
    A device used to hold multiple decks of cards typically 4, 6 or 8.
    Cards are dealt one at a time from the shoe.
    """

    def __init__(self):
        super().__init__()
        self._decks: List[CardDeck] = [] # The CardDecks in the CardShoe
        self._cards: List[PlayingCard] = [] # The PlayingCards in the CardShoe
        self.__discard: List[PlayingCard] = [] # All discarded PlayingCards

    @property
    def cards(self) -> tuple:
        """
        Property getter: Points to all of the `PlayingCard`s in the `CardShoe`.
        """
        return tuple(self._cards)

    @property
    def discards(self) -> tuple:
        """
        Property getter: Points to all discarded `PlayingCard`s.
        """
        return tuple(self.__discard)

    def _reload(self) -> None:
        """
        Move any discarded `PlayingCard`s back into the CardShoe.
        """
        self._cards.extend(self.__discard)
        self.__discard = []
        self.log.info('reloaded')

    def load(self, n_decks: int = 0) -> None:
        """
        Load the `CardShoe` with any number, N, `CardDeck`s.
        """
        # Check to see if existing CardDecks can be re-used.
        if n_decks == len(self._decks):
            self._reload()
            return
        # Create new CardDecks, as needed.
        for _ in range(n_decks):
            deck = CardDeck() # Create a CardDeck.
            self._decks.append(deck) # Reference the CardDeck.
            self._cards += deck.cards # Add the PlayingCards to the CardShoe.

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
        try:
            return self._cards.pop() # Draw a PlayingCard.
        except IndexError:
            return None # The CardShoe is empty.

    def discard(self, card: PlayingCard) -> None:
        """
        Discard a `PlayingCard` handed to `CardDealer`.
        """
        self.__discard.append(card)


__all__ = ['PlayingCard', 'CardDeck', 'CardShoe']
