from dataclasses import *
from typing import *

from .. import GameObject, PlayingCard
from . import CasinoToken


@dataclass
class CardHand(GameObject):
    """
    A dataclass representing a single `CardHand` of `PlayingCard`s.
    """

    player: "CardPlayer" # The CardPlayer the CardHand is assigned to
    bet: List[CasinoToken] = field(default_factory=list)
    _cards: List[PlayingCard] = field(default_factory=list) # All PlayingCards

    @classmethod
    def gen(cls, player: "CardPlayer", n_hands: int = 1) -> tuple:
        """
        A classmethod used to generate any number, N, of `CardHand`s.
        """
        # Generate N CardHands.
        if n_hands == 1:
            cls.log.debug('generating an empty CardHand for %s' % player)
            return (cls(player),)
        elif n_hands > 1:
            cls.log.debug('generating %i empty CardHands for %s' \
                          % (n_hands, player))
            return tuple(cls(player) for _ in range(n_hands))
        else:
            cls.log.error("can't generate no hands") # N = 0

    @property
    def cards(self) -> tuple:
        """
        Property getter: Points to the `PlayingCard`s in the `CardHand`.
        """
        return tuple(self._cards)

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

    def hit(self, card: PlayingCard) -> None:
        """
        Add a `PlayingCard` to the `CardHand`.
        """
        assert isinstance(card, PlayingCard), 'supplied card not a PlayingCard'
        self._cards.append(card)
        card.hand = self # Reference this CardHand from the PlayingCard.
        self.log.debug('card added: %s' % card)

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
            self.log.debug('card discarded: ' + repr(card))
        else:
            # Discard all PlayingCards from the CardHand.
            for card in self.cards:
                card.discard()
            self.log.debug('discarded')


__all__ = ['CardHand', 'PlayingCard']
