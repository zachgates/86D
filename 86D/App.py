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
        # Configure logging
        self.log.setLevel(self.settings.LOG_LEVEL.upper())
        formatter = logging.Formatter(self.settings.LOG_STYLE)
        # Configure a log file.
        if self.settings.LOG_STORE:
            mode = 'a' if self.settings.LOG_CACHE else 'w'
            file_handler = logging.FileHandler(self.settings.LOG_FNAME, mode=mode)
            file_handler.setFormatter(formatter)
            self.log.addHandler(file_handler)
        # Configure the console.
        if not self.settings.LOG_QUIET:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.log.addHandler(console_handler)
        # Notify
        self.log.info('starting.')


builtins.App = App = App()
__all__ = ['App']
