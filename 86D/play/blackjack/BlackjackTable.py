from ...core import CardTable
from . import BlackjackGame, BlackjackDealer


class BlackjackTable(CardTable):

    GameType = BlackjackGame
    DealerType = BlackjackDealer
