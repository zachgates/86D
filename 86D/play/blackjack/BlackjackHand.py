from ...core import CardHand


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
        return (len(self.cards) == 2 # Contains two cards:
                and any(card.rank == 0 for card in self.cards) # Ace
                and any(card.score == 10 for card in self.cards)) # "10"


__all__ = ['BlackjackHand']
