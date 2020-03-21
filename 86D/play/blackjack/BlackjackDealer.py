from ...core import gameclass, CardDealer
from . import BlackjackHand


@gameclass
class BlackjackDealer(CardDealer):

    HandType = BlackjackHand

    def load(self):
        # Load the CardShoe with N-1 decks where N is the number of CardPlayers
        super().load(len(self.table.game.players) - 1)

    def deal(self):
        # First round deal
        self.log.debug('first round deal.')
        for player in reversed(self.table.players):
            self.hit(player)
        # Second round deal
        self.log.debug('second round deal.')
        for player in reversed(self.table.players):
            self.hit(player, reveal=True)

    def insurance(self):
        # CardDealer is showing an ace.
        if self.hand(0).cards[1].rank == 0:
            # TODO: Ask CardPlayers for insurance bets
            self.log.info('showing an ace; accepting insurance bets.')
            # Reveal CardDealer's hand.
            self.hand(0).up = True
            # Handle CardDealer blackjack.
            if self.hand(0).blackjack:
                self.log.info('blackjack: %s.' % self.hand(0))
                for player in self.table.players[1:]: # Exclude CardDealer.
                    # Reveal CardPlayer's hand.
                    hand = player.hand(0)
                    hand.up = True
                    if hand.blackjack or hand.insured:
                        # CardPlayer receives bets if insured or blackjack.
                        self.log.debug('%s receives bets back.' % player)
                        self.win(hand)
                    else:
                        # Bets are collected otherwise.
                        self.log.debug('%s loses bets.' % player)
                        self.lose(hand)


__all__ = ['BlackjackDealer']
