from dataclasses import *
from typing import *

from .. import gameclass, GameObject, PlayingCard, CardSet
from . import CasinoToken


@gameclass
class CardHand(CardSet):
    """
    A dataclass representing a single `CardHand` of `PlayingCard`s.
    """

    player: "CardPlayer" = None # The CardPlayer the CardHand is assigned to
    _bet: List[CasinoToken] = field(default_factory=list)
    _cards: List[PlayingCard] = field(default_factory=list) # All PlayingCards

    def __post_init__(self):
        self._assert(self.player, 'CardHand must be assigned to CardPlayer')

    @classmethod
    def gen(cls, player: "CardPlayer", n_hands: int = 1) -> tuple:
        """
        A classmethod used to generate any number, N, of `CardHand`s.
        """
        # Generate N CardHands.
        if n_hands == 1:
            cls.log.debug('generating an empty CardHand for %s.' % player)
            return [cls(player=player)]
        elif n_hands > 1:
            cls.log.debug('generating %i empty CardHands for %s.' \
                          % (n_hands, player))
            return [cls.gen(player) for _ in range(n_hands)]
        else:
            self._assert(False, "can't generate no hands.") # N = 0


__all__ = ['CardHand']
