from ...core import CardGame


class BlackjackGame(CardGame):

    def play(self):
        super().play()
        self.insurance()

    def insurance(self):
        # CardDealer is showing an ace.
        hand = self.dealer.hand(0)
        if hand.cards[1].rank == 0:
            # TODO: Ask CardPlayers for insurance bets.
            self.log.info('showing an ace; accepting insurance bets.')
            # Reveal CardDealer's hand.
            hand.up = True
            # Handle CardDealer blackjack.
            if hand.blackjack:
                self.log.info('blackjack: %s.' % hand)
                for player in self.players: # Exclude CardDealer.
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
