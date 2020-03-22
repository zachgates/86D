import builtins
import logging

from . import __name__, LOG, SETTINGS


class _(object):

    SETTINGS = SETTINGS

    def __init__(self):
        # Configure logging
        LOG.setLevel(SETTINGS.LOG_LEVEL.upper())
        formatter = logging.Formatter(SETTINGS.LOG_STYLE)
        # Configure a log file.
        if SETTINGS.LOG_FNAME is not None:
            mode = 'a' if SETTINGS.LOG_CACHE else 'w'
            file_handler = logging.FileHandler(SETTINGS.LOG_FNAME, mode=mode)
            file_handler.setFormatter(formatter)
            LOG.addHandler(file_handler)
        # Configure the console.
        if not SETTINGS.LOG_QUIET:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            LOG.addHandler(console_handler)
        # Notify
        LOG.info('starting.')

    def run(self):
        from .core import CardTable, CardPlayer
        from .play.blackjack import BlackjackGame, BlackjackDealer
        p1 = CardPlayer(funds=5000)
        p2 = CardPlayer(funds=5000)
        t = CardTable(BlackjackGame, BlackjackDealer)
        t.add_player(p1)
        t.add_player(p2)
        b1 = t.gather_bet(p1, 513)
        b2 = t.gather_bet(p2, 201)
        t.game.play()
        t.remove_player(p1)
        t.remove_player(p2)


# Environment variable.
builtins.LOG = LOG
builtins.APP = _()
# Execute.
APP.run()
