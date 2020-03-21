from ...core import gameclass, CardHand


@gameclass
class BlackjackHand(CardHand):
    """
    A dataclass representing a single BlackjackHand type of CardHand.
    """

    insured: bool = False # Indicates CardHand "insurance" against CardDealer

    @property
    def blackjack(self):
        """
        Property getter: Points to whether a `BlackjackHand` is a blackjack.
        """
        if len(self.cards) == 2: # Contains: two cards,
            if any(card.rank == 0 for card in self.cards): # Ace,
                if any(card.rank >= 9 for card in self.cards): # Rank 10;
                    return True # Blackjack!
        return False


__all__ = ['BlackjackHand']
