from dataclasses import field
from typing import List

from .. import gameclass, GameObject
from . import CasinoToken, CardDealer


@gameclass
class CardTable(GameObject):

    MaxPlayers = 7 # "the usual 'full table'"
    MinPlayers = 2

    dealer_type: type
    _dealer: CardDealer = None
    _players: List["CardPlayer"] = field(default_factory=list)
    _waiting: List["CardPlayer"] = field(default_factory=list)

    def __post_init__(self):
        """
        Create and assign the `CardTable`'s `CardDealer`.
        """
        self._in_play: bool = False # Active gameplay indicator
        self._assert(issubclass(self.dealer_type, CardDealer),
                    'dealer_type must be CardDealer or subclass.')
        self._dealer = self.dealer_type(self)

    @property
    def active(self) -> bool:
        """
        Property getter: Boolean representing whether gameplay has begun.
        """
        return bool(self._in_play)

    @property
    def dealer(self):
        """
        Property getter: Points to the `CardTable`'s `CardDealer`.
        """
        return self._dealer

    @property
    def players(self):
        """
        Property getter: Points to a single-dimensional tuple that contains the
        `CardTable`'s `CardDealer` and its "player record" of `CardPlayer`s.
        """
        return (self._dealer,) + tuple(self._players)

    @property
    def seated(self):
        """
        Property getter: Points to a single-dimensional tuple that contains the
        `CardTable`'s `CardDealer`, the "player record" of `CardPlayer`'s,
        and the "waiting players record" of `CardPlayer`s, in that order.
        """
        return self.players + tuple(self._waiting)

    def add_player(self, player: "CardPlayer"):
        """
        Try to seat a `CardPlayer` at this `CardTable`.
        """
        # Check for empty seats
        self._assert(len(self.seated) < self.MaxPlayers, 'no seats available.')

        # If gameplay has begun, seat the CardPlayer, but as "waiting".
        if self.active:
            self._waiting.append(player)
            player.waiting = True
        # If no game is in play, add the CardPlayer to the "player record".
        else:
            self._players.append(player)
            player.waiting = False
            player.hands = self.dealer.HandType.gen(player)

        # Assign this CardTable to the CardPlayer.
        player.table = self

    def remove_player(self, player: "CardPlayer"):
        """
        Remove a seated `CardPlayer` from this `CardTable`.
        """
        # Remove a CardPlayer who is seated, but waiting.
        if player in self._waiting:
            self.log.debug('%r stopped waiting.' % player)
            self._waiting.remove(player)
        # Remove a seated CardPlayer from a game.
        elif player in self._players:
            self.log.debug('remove_player(%r)' % player)
            # Discard any CardHands that the CardPlayer holds.
            self.dealer.discard(hands=player.hands)
            player.hands = []
            # Remove the CardPlayer from the "player record".
            self._players.remove(player)
            # Unassign this CardTable from the CardPlayer.
            player.table = None
        else:
            # CardPlayer supplied is not assigned this CardTable.
            self._assert(False, 'CardPlayer is not even seated.')

        # Check if any CardPlayers are seated, aside from the CardDealer.
        if self.players == (self.dealer,) and self.active:
            self._in_play = False # CardTable indicates gameplay has ended.
            self.dealer.reset() # CardDealer empties the CardShoe.

    def gather_bet(self, player: "CardPlayer", value: int):
        """
        Generate the necessary `CasinoToken`s for the `CardPlayer`'s bet.
        """
        # Evaluate the CardPlayer's funds.
        if player.funds < value:
            self._assert(False, '%r has too few funds. tried betting ($%i).' \
                                % (player, value), warn=True)
            return
        # Generate the necessary CasinoTokens.
        self.log.info('generating ($%i) in CasinoTokens.' % value)
        player._funds -= value
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

    def play(self):
        """
        Indicate and begin gameplay with seated `CardPlayer`s.
        """
        # Check if a game is in play at this CardTable.
        if self.active:
            self._assert(False, 'game is already in play.')
            return
        # Ensure enough players are seated.
        if (len(self.players) >= self.MinPlayers):
            self._in_play = True  # Indicate CardTable is active.
            self.dealer.play()
        else:
            self._assert(False, 'too few players to begin.', warn=True)


__all__ = ['CardTable']
