from .. import GameObject


class CardTable(GameObject):

    MaxPlayers: int = 7 # "the usual 'full table'"
    MinPlayers: int = 2

    def __init__(self, dealer_type: type):
        self._in_play: bool = False # Active gameplay indicator
        self._dealer: CardDealer = None
        self.__dealer_type = dealer_type # Supplied by superclass
        assert callable(self.__dealer_type) and isinstance(dealer_type, type)
        self.__players: List[CardPlayer] = [] # Players seated and in gameplay
        self.__waiting: List[CardPlayer] = [] # Players seated and waiting

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
        if self._dealer is None:
            # Create and assign a dealer. Executes upon first reference.
            self._dealer = self.__dealer_type(self)
        return self._dealer

    @property
    def players(self):
        """
        Property getter: Points to a single-dimensional tuple that contains the
        `CardTable`'s `CardDealer` and its "player record" of `CardPlayer`s.
        """
        return (self._dealer,) + tuple(self.__players)

    @property
    def seated(self):
        """
        Property getter: Points to a single-dimensional tuple that contains the
        `CardTable`'s `CardDealer`, the "player record" of `CardPlayer`'s,
        and the "waiting players record" of `CardPlayer`s, in that order.
        """
        return self.players + tuple(self.__waiting)

    def add_player(self, player: "CardPlayer"):
        """
        Try to seat a `CardPlayer` at this `CardTable`.
        """
        # Check for empty seats
        if len(self.seated) == self.MaxPlayers:
            self.log.warning('no seats available') # The CardTable is full.
            return

        # If gameplay has begun, seat the CardPlayer, but as "waiting".
        if self.active:
            self.__waiting.append(player)
            player.waiting = True
        # If no game is in play, add the CardPlayer to the "player record".
        else:
            self.__players.append(player)
            player.waiting = False

        # Assign this CardTable to the CardPlayer.
        player.table = self

    def remove_player(self, player: "CardPlayer"):
        """
        Remove a seated `CardPlayer` from this `CardTable`.
        """
        # Remove a CardPlayer who is seated, but waiting.
        if player in self.__waiting:
            self.__waiting.remove(player)
        # Remove a seated CardPlayer from a game.
        elif player in self.__players:
            # Discard any CardHands that the CardPlayer holds.
            self.dealer.discard(hands=player.hands)
            player.hands = []
            # Remove the CardPlayer from the "player record".
            self.__players.remove(player)
            # Unassign this CardTable from the CardPlayer.
            player.table = None
        else:
            # CardPlayer supplied is not assigned this CardTable.
            self.log.critical('CardPlayer is not even seated')

        # Check if any CardPlayers are seated, aside from the CardDealer.
        if set(self.players) == {self.dealer}:
            self._in_play = False # CardTable indicates gameplay has ended.
            self.dealer.reset() # CardDealer empties the CardShoe.
            
    def _play(self):
        """
        Run a single frame of gameplay. Override in subclass.
        """
        pass

    def play(self):
        """
        Indicate and begin gameplay with seated `CardPlayer`s.
        """
        # Sanity check
        if self.active:
            self.log.critical('game is already in play')

        # Ensure enough players are seated.
        if (len(self.players) >= self.MinPlayers):
            self._in_play = True  # Indicate CardTable is active.
            self.dealer.play()
        else:
            self.log.warning('too few players to begin')


__all__ = ['CardTable']
