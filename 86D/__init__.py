import argparse
import logging


parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-f', '--style', type=str,
                    default='[%(levelname)8s] | %(name)-25s: %(message)s')
parser.add_argument('-l', '--level', type=str, default='INFO')
parser.add_argument('-t', '--trace', action='store_true')
args = parser.parse_args()

VERBOSE = args.verbose
LOG_LEVEL = getattr(logging, args.level.upper())
LOG_TRACE = args.trace
_LOG_OPTS = {
    'format': args.style,
    'level': LOG_LEVEL,
}

if not VERBOSE:
    _LOG_OPTS.update({'filename': '%s.log' % __name__, 'filemode': 'w'})
logging.basicConfig(**_LOG_OPTS)


__all__ = ['VERBOSE', 'LOG_LEVEL', 'LOG_TRACE']
