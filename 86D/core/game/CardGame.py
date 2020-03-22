from typing import List

from dataclasses import dataclass, field

from .. import GameObject


class CardGame(GameObject):
    """
    A dataclass representing a single game.
    """

    dealer: "CardDealer"
    players: List["CardPlayer"] = field(default_factory=list)

    def __post_init__(self):
        self._in_play = False

    @property
    def active(self):
        return (self.players and self._in_play)

    def add_player(self, player: "CardPlayer"):
        self.log.info('%r joined.' % player)
        self.players.append(player)
        player.hands = [self.dealer.HandType([], player)]

    def remove_player(self, player: "CardPlayer"):
        self.log.info('%r quit.' % player)
        self.dealer.discard(player)
        player.hands = []
        self.players.remove(player)

    def play(self):
        # Check if this CardGame is already in play.
        if self.active:
            self._assert(False, 'game is already in play.')
            return
        # Ensure enough players are seated.
        self._assert(self.players, 'no players.', warn=True)
        # Start the CardGame.
        self.log.info('starting.')
        self._in_play = True
        self.dealer.load()
        self.dealer.shuffle()
        self.dealer.deal()
        ...

    def win(self, hand: "CardHand", player: "CardPlayer" = None):
        """
        Contains the logic for winning a `hand`. If no `hand` is supplied, then
        a `player` must be supplied. `CardHand`s the supplied `CardPlayer` holds
        are assumed to have won.
        """
        if player is not None:
            self._assert(isinstance(player, CardPlayer), 'player not a CardPlayer.')
            for hand in player.hands:
                self.win(hand)
        else:
            self._assert(hand.player, 'CardHand has no assigned CardPlayer.')
            hand.player.log.info('winning hand: %s.' % hand)

    def lose(self, hand: "CardHand", player: "CardPlayer" = None):
        """
        Contains the logic for losing a `hand`. If no `hand` is supplied, then
        a `player` must be supplied. `CardHand`s the supplied `CardPlayer` holds
        are assumed to have lost.
        """
        if player is not None:
            self._assert(isinstance(player, CardPlayer), 'player not a CardPlayer.')
            for hand in player.hands:
                self.lose(hand)
        else:
            self._assert(hand.player, 'CardHand has no assigned CardPlayer.')
            hand.player.log.info('losing hand: %s.' % hand)

    def cleanup(self):
        """
        Clean up a finished `CardGame`.
        """
        self.dealer.reset() # CardDealer empties the CardShoe.
        self.log.info('done.')
