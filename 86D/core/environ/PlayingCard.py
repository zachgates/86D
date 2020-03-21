from .. import gameclass, GameObject


@gameclass
class PlayingCard(GameObject):
    """
    A dataclass representing a single `PlayingCard` in a `CardDeck`.
    """

    SuitRange = range(4)
    SuitNames = ['spades', 'hearts', 'diamonds', 'clubs']
    RankRange = range(13)
    RankNames = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven',
                 'eight', 'nine', 'ten', 'jack', 'queen', 'king']

    rank: int # Indicates the PlayingCard's rank, range(13)
    suit: int # Indicates the PlayingCard's suit, range(4)
    deck: "CardDeck" = None # Points to the PlayingCard's CardDeck
    hand: "CardHand" = None # Points to the (optional) PlayingCard's CardHand
    up: bool = False # Indicates an "upcard" (face-up)

    def __eq__(self, other):
        """
        `PlayingCard` equality tests compare `PlayingCard` rank and suit.
        """
        return (self.rank, self.suit) == (other.rank, other.suit)

    def __str__(self):
        """
        Render a `PlayingCard` to a human-readable string.
        """
        if self.up:
            return '<%s of %s>' % (
                self.RankNames[self.rank],
                self.SuitNames[self.suit])
        else:
            return '<***>'

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
        self.log.debug('discard()')


__all__ = ['PlayingCard']
