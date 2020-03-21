def gameclass(cls):
    """
    A decorator for dataclasses.
    """
    from dataclasses import dataclass
    return dataclass(repr=False, eq=False)(cls)


from .GameObject import GameObject
from .environ import PlayingCard, CardSet, CardDeck, CardShoe
from .game import CasinoToken, CardGame, CardHand, CardPlayer, CardDealer, CardTable


__all__ = ['gameclass',
           'GameObject',
           'PlayingCard', 'CardSet', 'CardDeck', 'CardShoe',
           'CasinoToken', 'CardGame', 'CardHand', 'CardPlayer', 'CardDealer', 'CardTable']
