from ...core import CardDealer
from . import BlackjackHand


class BlackjackDealer(CardDealer):

    HandType = BlackjackHand

    def load(self):
        # Load the CardShoe with N decks where N is the number of CardPlayers.
        super().load(len(self.table.game.players))

    def deal(self):
        # First round deal
        self.log.debug('first round deal.')
        for player in reversed(self.table.players):
            self.hit(player)
        # Second round deal
        self.log.debug('second round deal.')
        for player in reversed(self.table.players):
            self.hit(player, reveal=True)


__all__ = ['BlackjackDealer']
