from typing import List

from dataclasses import dataclass, field

from .. import gameclass, GameObject


@gameclass
class CardGame(GameObject):
    """
    A dataclass representing a single game.
    """

    dealer: "CardDealer"
    players: List["CardPlayer"] = field(default_factory=list)
    active: bool = False

    def add_player(self, player: "CardPlayer"):
        self.players.append(player)
        player.hands = self.dealer.HandType.gen(player)

    def remove_player(self, player: "CardPlayer"):
        self.log.debug('remove_player(%r)' % player)
        self.dealer.discard(player)
        player.hands = []
        self.players.remove(player)
        self.active = bool(self.players)

    def play(self):
        # Check if a game is in play at this CardTable.
        if self.active:
            self._assert(False, 'game is already in play.')
            return
        # Ensure enough players are seated.
        self._assert(self.players, 'no players.', warn=True)
        # Start the CardGame.
        self.log.info('play()')
        self.active = True
        self.dealer.load()
        self.dealer.shuffle()
        self.dealer.deal()
        ...
