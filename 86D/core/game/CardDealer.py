from dataclasses import field
from typing import List

from .. import gameclass, PlayingCard
from . import CardHand, CardPlayer


@gameclass
class CardDealer(CardPlayer):
    """
    Deals cards from a special device called a "dealer's shoe".
    """

    HandType = CardHand

    def __post_init__(self):
        """
        Initialize the `CardDealer` with an empty `CardHand`.
        """
        self._drawn = []
        self.hands = [self.HandType([], self)]

    @property
    def deck(self):
        """
        Property pointing to `PlayingCard`s in the `CardDealer`'s `CardShoe`.
        """
        return tuple(self.table.shoe.cards)

    def load(self, n_decks: int = 1):
        """
        `CardDealer` loads the `CardShoe` with N `CardDeck`s; default is one.
        """
        self.table.shoe.load(n_decks)
        self.log.info('loaded (%i) CardDecks into the CardShoe.' % n_decks)

    def shuffle(self):
        """
        `CardDealer` shuffles the `PlayingCard`s in the `CardShoe`.
        """
        self.table.shoe.shuffle()
        self.log.info('shuffled.')

    def draw(self, reveal: bool = False, n_cards: int = 1) -> PlayingCard:
        """
        `CardDealer` draws a `PlayingCard` from the `CardShoe`, with the
        option to `reveal` the card, face-up.

        Keyword arguments:
        reveal -- a boolean representing whether the `PlayingCard` is face-up
        """
        card = self.table.shoe.draw() # Draw a PlayingCard from the CardShoe.
        self._drawn.append(card) # Add it to the "drawn record".
        card.up = reveal
        self.log.debug('draw() -> %r' % card)
        return card

    def deal(self):
        """
        Implement deal logic in a subclass.
        """
        self._assert(False, 'deal logic should be implemented in subclass.')

    def __discard(self, card: PlayingCard = None, n_cards: int = 0):
        """
        Discard either a single `PlayingCard`, or a number, N, `PlayingCard`s,
        from the `CardShoe`, but not both. Where `n_cards == -1`, any
        `PlayingCard`s remaining in the `CardShoe` are discarded.

        Keyword arguments:
        card -- a single `PlayingCard`
        n_cards -- an integer representing any number of `PlayingCard`s
        """
        # Remove the supplied PlayingCard from the "drawn record".
        if card:
            # Verify the supplied PlayingCard is in the "drawn record".
            self._assert(card in self._drawn, '%r not drawn by me.' % card)
            card.discard()
            self._drawn.remove(card)
            self.table.shoe.discard(card)
        # No PlayingCard supplied to discard.
        else:
            # Ensure n_cards is set if no card was supplied.
            self._assert(n_cards, 'no card supplied assumes n_cards != 0.',
                         warn=True)
            # Discard any number, N, PlayingCards from the CardShoe.
            cards = []
            while n_cards > 0:
                # Attempt to draw a PlayingCard from the CardShoe.
                card = self.draw()
                # Check if enough PlayingCards in CardShoe to complete action.
                if not card:
                    self._assert(False, 'not enough PlayingCards in CardShoe.',
                                 warn=True)
                    break
                else:
                    cards.append(card)
                n_cards -= 1
            # Discard all remaining PlayingCards in the CardShoe.
            if n_cards < 0:
                while self.deck:
                    card = self.table.shoe.draw()
                    self.table.shoe.discard(card)
                return
            # Repeat with selected PlayingCards.
            self.discard(cards=cards)

    def discard(self,
                player: CardPlayer = None,
                cards: List[PlayingCard] = [],
                n_cards: int = 0):
        """
        Discard `PlayingCard`s from the `CardShoe` in three distinct ways.
        Where `n_cards == -1`, any `PlayingCard`s remaining in the `CardShoe`
        are discarded.

        Keyword arguments:
        player -- a `CardPlayer` of who's `CardHand`s to dicard
        cards -- a list of `PlayingCard`s
        n_cards -- an integer representing any number of `PlayingCard`s
        """
        # Discard any CardHands a CardPlayer holds.
        if player:
            self.log.info('discarding %r cards.' % player)
            self._assert(isinstance(player, CardPlayer), 'player not a CardPlayer')
            for hand in player.hands:
                hand.discard()
        # Discard PlayingCards handed to the CardDealer.
        for card in cards[:]:
            self.__discard(card=card)
        # Discard N PlayingCards from the CardShoe.
        if n_cards:
            self.__discard(n_cards=n_cards)

    def reset(self):
        """
        Discard old `CardDeck`s.
        """
        # Discard any PlayingCards the CardDealer may hold.
        self.discard(player=self)
        # Register how many remaining PlayingCards will be discarded.
        n_cards = len(self.deck)
        # Discard any PlayingCards held by CardPlayers, and remaining CardDeck.
        self.discard(cards=tuple(self._drawn), n_cards=-1)
        # Reset the "drawn record".
        self._drawn = []
        self.log.debug('discarded (%i) PlayingCards from %r.' % (n_cards, self.table.shoe))

    def hit(self, player: CardPlayer, hand_ord: int = 0, reveal: bool = False):
        """
        Draw and add a PlayingCard to a CardHand of a CardPlayer.

        Keyword arguments:
        hand_ord -- An integer indicating the index of the CardHand. Default 0.
        reveal -- A boolean representing the orientation of the PlayingCard.
        """
        card = self.draw(reveal)
        hand = player.hand(hand_ord)
        hand.add(card)
        player.log.info('hand(%i).add(%s)' % (hand_ord, card))


__all__ = ['CardDealer']
