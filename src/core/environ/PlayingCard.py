from dataclasses import *

from .. import GameObject


@dataclass
class PlayingCard(GameObject):
    """
    A dataclass representing a single `PlayingCard` in a `CardDeck`.
    """

    SUIT_ORDS = range(4)
    SUIT_NAMES = ['spades', 'hearts', 'diamonds', 'clubs']
    RANK_ORDS = range(13)
    RANK_NAMES = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven',
                  'eight', 'nine', 'ten', 'jack', 'queen', 'king']

    rank: int # Indicates the PlayingCard's rank, range(13)
    suit: int # Indicates the PlayingCard's suit, range(4)
    deck: "CardDeck" = None # Points to the PlayingCard's CardDeck
    hand: "CardHand" = None # Points to the (optional) PlayingCard's CardHand
    up: bool = False # Indicates an "upcard" (face-up)

    def __repr__(self):
        if self.up:
            return '<%s of %s>' % (
                PlayingCard.RANK_NAMES[self.rank],
                PlayingCard.SUIT_NAMES[self.suit])
        else:
            return '<***>'

    def __eq__(self, other):
        """
        Compare `PlayingCard`s by their rank and suit.
        """
        return (self.rank, self.suit) == (other.rank, other.suit)

    @property
    def score(self):
        """
        Property getter: Points to the score of a PlayingCard.
        """
        return min(self.rank + 1, 10)

    def discard(self):
        """
        Reveal the `PlayingCard` and discard it.
        """
        # Reveal the PlayingCard.
        self.up = True
        # Unassign any CardHand.
        if self.hand is not None:
            self.hand.discard(self)
        self.log.debug('discarded')


__all__ = ['PlayingCard']
