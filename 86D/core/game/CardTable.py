from dataclasses import field
from typing import List

from .. import gameclass, GameObject, CardShoe
from . import CasinoToken, CardGame, CardPlayer, CardDealer


@gameclass
class CardTable(GameObject):

    MaxPlayers = 7 # "the usual 'full table'"
    MinPlayers = 2

    game_type: type
    dealer_type: type
    waiting: List[CardPlayer] = field(default_factory=list)

    def __post_init__(self):
        """
        Create and assign the `CardTable`'s `CardDealer`.
        """
        # Create the CardShoe.
        self.shoe = CardShoe()
        # Create the CardDealer.
        self._assert(issubclass(self.dealer_type, CardDealer),
                    'dealer_type must be CardDealer or subclass.')
        dealer = self.dealer_type()
        dealer.table = self
        # Create the CardGame.
        self._assert(issubclass(self.game_type, CardGame),
                    'game_type must be subclass of CardGame.')
        self.game = self.game_type(dealer)
        self.log.info('generated %r with %r.' % (self.game, dealer))

    @property
    def dealer(self):
        """
        Property getter: Points to the `CardGame`'s `CardDealer`.
        """
        return self.game.dealer

    @property
    def players(self):
        """
        Property getter: Points to a single-dimensional tuple that contains the
        `CardTable`'s `CardDealer` and its "player record" of `CardPlayer`s.
        """
        return (self.dealer,) + tuple(self.game.players)

    @property
    def seated(self):
        """
        Property getter: Points to a single-dimensional tuple that contains the
        `CardTable`'s `CardDealer`, the "player record" of `CardPlayer`'s,
        and the "waiting players record" of `CardPlayer`s, in that order.
        """
        return self.players + tuple(self.waiting)

    def add_player(self, player: CardPlayer):
        """
        Try to seat a `CardPlayer` at this `CardTable`.
        """
        self.log.debug('%r joining.' % player)
        # Check for empty seats
        self._assert(len(self.seated) < self.MaxPlayers, 'no seats available.')

        # If gameplay has begun, seat the CardPlayer, but as "waiting".
        if self.game.active:
            self.waiting.append(player)
            player.waiting = True
            self.log.debug('%r waiting to play.' % player)
        # If no game is in play, add the CardPlayer to the "player record".
        else:
            player.waiting = False
            self.game.add_player(player)

        # Assign this CardTable to the CardPlayer.
        player.table = self

    def remove_player(self, player: CardPlayer):
        """
        Remove a seated `CardPlayer` from this `CardTable`.
        """
        self.log.debug('%r leaving.' % player)
        if player in self.game.players:
            self.game.remove_player(player)
            player.table = None
        elif player in self.waiting:
            self.log.debug('%r stopped waiting.' % player)
            self.waiting.remove(player)
        else:
            self._assert(False, 'CardPlayer not even seated.')

        # Check if any CardPlayers are seated, aside from the CardDealer.
        if not self.game.active:
            self.game.cleanup()

    def gather_bet(self, player: CardPlayer, value: int):
        """
        Generate the necessary `CasinoToken`s for the `CardPlayer`'s bet.
        """
        # Evaluate the CardPlayer's funds.
        if player.funds < value:
            self._assert(False, '%r has too few funds. tried betting ($%i).' \
                                % (player, value), warn=True)
            return
        # Generate the necessary CasinoTokens.
        self.log.info('generating ($%i) in CasinoTokens for %r.' % (value, player))
        player.funds -= value
        tokens = []
        # Decompose the bet value.
        while value:
            for val in reversed(CasinoToken.TokenValues):
                if value % val == 0:
                    tokens.append(CasinoToken(val))
                    value -= val
                    break
        # Return the required CasinoTokens as a tuple from least to greatest.
        return tokens


__all__ = ['CardTable']
