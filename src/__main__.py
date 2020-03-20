import logging

from . import VERBOSE, LOG_LEVEL
from .core import CardPlayer
from .play import BlackjackTable


def main():
    p1 = CardPlayer()
    p2 = CardPlayer()
    t = BlackjackTable()
    t.add_player(p1)
    t.add_player(p2)
    t.play()
    t.remove_player(p1)
    t.remove_player(p2)


if __name__ == '__main__':
    # Setup logging.
    if VERBOSE:
        # Output to console.
        logging.basicConfig(level=LOG_LEVEL)
    else:
        # Output to file.
        fname = __name__ + '.log'
        logging.basicConfig(level=LOG_LEVEL, filename=fname, filemode='w')
    # Execute test case.
    main()
