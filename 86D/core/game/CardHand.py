from typing import List

from .. import gameclass, CardSet
from . import CardPlayer


@gameclass
class CardHand(CardSet):
    """
    A dataclass representing a single `CardHand` of `PlayingCard`s.
    """

    player: CardPlayer
    bet: int = 0


__all__ = ['CardHand']
