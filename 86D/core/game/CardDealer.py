from dataclasses import *
from typing import *

from .. import gameclass, PlayingCard, CardShoe
from . import CardHand, CardPlayer


@gameclass
class CardDealer(CardPlayer):
    """
    Deals cards from a special device called a "dealer's shoe".
    """

    _shoe: CardShoe = CardShoe()
    _drawn: List[PlayingCard] = field(default_factory=list)

    def __init__(self, table: "CardTable"):
        """
        Initialize the `CardDealer` with an empty `CardShoe` and empty "drawn
        record". Assign them a `CardTable`.
        """
        super().__init__()
        self.table = table

    @property
    def deck(self):
        """
        Property pointing to `PlayingCard`s in the `CardDealer`'s `CardShoe`.
        """
        return tuple(self._shoe.cards)

    def play(self):
        """
        `CardDealer` loads the `CardShoe`, shuffles, and deals. Additional
        gameplay logic should be defined in the `_play` method.
        """
        self.load()
        self.shuffle()
        self.deal()
        ...

    def load(self, n_decks: int = 1):
        """
        `CardDealer` loads the `CardShoe` with N `CardDeck`s; default is one.
        """
        self._shoe.load(n_decks)
        self.log.debug('loaded (%i) CardDecks into the CardShoe.' % n_decks)

    def shuffle(self):
        """
        `CardDealer` shuffles the `PlayingCard`s in the `CardShoe`.
        """
        self._shoe.shuffle()
        self.log.debug('shuffled.')

    def draw(self, reveal: bool = False, n_cards: int = 1) -> PlayingCard:
        """
        `CardDealer` draws a `PlayingCard` from the `CardShoe`, with the
        option to `reveal` the card, face-up.

        Keyword arguments:
        reveal -- a boolean representing whether the `PlayingCard` is face-up
        """
        card = self._shoe.draw() # Draw a PlayingCard from the CardShoe.
        self._drawn.append(card) # Add it to the "drawn record".
        card.up = reveal
        self.log.debug('draw() -> %r' % card)
        return card

    def deal(self):
        """
        Implement deal logic in a subclass.
        """
        self._assert(False, 'deal logic should be implemented in subclass.')
        ...

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
            self._shoe.discard(card)
        # No PlayingCard supplied to discard.
        else:
            # Ensure n_cards is set if no card was supplied.
            self._assert(n_cards, 'no card supplied assumes n_cards != 0.')
            # Discard any number, N, PlayingCards from the CardShoe.
            cards = []
            while n_cards > 0:
                # Attempt to draw a PlayingCard from the CardShoe.
                card = self.draw()
                # Check if enough PlayingCards in CardShoe to complete action.
                self._assert(card, 'not enough PlayingCards in CardShoe.')
                cards.append(card)
                n_cards -= 1
            else:
                if n_cards < 0:
                    # Discard all remaining PlayingCards in the CardShoe.
                    while self.deck:
                        cards.append(self.draw())
                # Repeat with selected PlayingCards.
                self.discard(cards=cards)

    def discard(self,
                hands: List[CardHand] = [],
                cards: List[PlayingCard] = [],
                n_cards: int = 0):
        """
        Discard `PlayingCard`s from the `CardShoe` in three distinct ways.
        Where `n_cards == -1`, any `PlayingCard`s remaining in the `CardShoe`
        are discarded.

        Keyword arguments:
        hands -- a list of `CardHand`s
        cards -- a list of `PlayingCard`s
        n_cards -- an integer representing any number of `PlayingCard`s
        """
        # Discard CardHands handed to the CardDealer.
        for hand in hands:
            self.log.debug('discard(%r)' % hand)
            self.discard(cards=hand.cards)
        # Discard PlayingCards handed to the CardDealer.
        for card in cards:
            self.__discard(card=card)
        # Discard N PlayingCards from the CardShoe.
        if n_cards:
            self.__discard(n_cards=n_cards)

    def reset(self):
        """
        Discard old `CardDeck`s.
        """
        # Discard any PlayingCards the CardDealer may hold.
        self.discard(hands=self.hands)
        # Register how many remaining PlayingCards will be discarded.
        n_cards = len(self.deck)
        # Discard any PlayingCards held by CardPlayers, and remaining CardDeck.
        self.discard(cards=tuple(self._drawn), n_cards=-1)
        # Reset the "drawn record".
        self._drawn = []
        self.log.debug('discarded (%i) PlayingCards from CardShoe.' % n_cards)

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
        self.log.info('%r.add(%s)' % (hand, card))

    def win(self, hand: CardHand, player: CardPlayer = None):
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

    def lose(self, hand: CardHand, player: CardPlayer = None):
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


__all__ = ['CardDealer', 'PlayingCard', 'CardHand', 'CardPlayer']
