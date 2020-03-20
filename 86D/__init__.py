import argparse
import logging


parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-l', '--level', type=str, default='INFO')
parser.add_argument('-t', '--trace', action='store_true')
args = parser.parse_args()

VERBOSE = args.verbose
LOG_LEVEL = getattr(logging, args.level)
LOG_TRACE = args.trace

# Output to console.
if VERBOSE:
    logging.basicConfig(level=LOG_LEVEL)
# Output to file.
else:
    fname = __name__ + '.log'
    logging.basicConfig(level=LOG_LEVEL, filename=fname, filemode='w')


__all__ = ['VERBOSE', 'LOG_LEVEL', 'LOG_TRACE']
