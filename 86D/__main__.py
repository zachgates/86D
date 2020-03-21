import builtins
import logging

from dataclasses import dataclass

from . import __name__, Settings


@dataclass
class App(object):
    """
    Dataclass representing the application itself.
    """

    log: logging.Logger = logging.getLogger(__name__)
    settings: Settings = Settings

    def __post_init__(self):
        # Add environment variables.
        builtins.App = self
        builtins.Log = App.log
        builtins.Settings = App.settings
        # Configure logging
        self.log.setLevel(Settings.LOG_LEVEL.upper())
        formatter = logging.Formatter(Settings.LOG_STYLE)
        # Configure a log file.
        if Settings.LOG_STORE:
            mode = 'a' if Settings.LOG_CACHE else 'w'
            file_handler = logging.FileHandler(Settings.LOG_FNAME, mode=mode)
            file_handler.setFormatter(formatter)
            Log.addHandler(file_handler)
        # Configure the console.
        if not Settings.LOG_QUIET:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            Log.addHandler(console_handler)
        # Notify
        Log.info('starting.')

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


App = App()
App.run()
