from ...core import CardHand


class BlackjackHand(CardHand):

    insured: bool = False # Indicates CardHand "insurance" against CardDealer

    def __str__(self):
        return '[%i] %s' % (self.score, super().__str__())

    @property
    def score(self) -> int:
        total = 0
        for card in self.cards:
            total += card.score
        return total

    @property
    def blackjack(self) -> bool:
        return (len(self.cards) == 2 # Contains two cards:
                and any(card.rank == 0 for card in self.cards) # Ace
                and any(card.score == 10 for card in self.cards)) # "10"

    @property
    def bust(self) -> bool:
        return self.score > 21


__all__ = ['BlackjackHand']
