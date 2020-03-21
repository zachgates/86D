import argparse

from dataclasses import dataclass

from . import __name__


@dataclass
class Settings(object):
    """
    A dataclass representing the application settings.
    """

    LOG_FNAME: str = None
    LOG_LEVEL: str = 'INFO'
    LOG_STYLE: str = '[%(levelname)8s] | %(name)-25s: %(message)s'
    LOG_TRACE: bool = False
    LOG_QUIET: bool = False
    LOG_STORE: bool = False
    LOG_CACHE: bool = False

    def __post_init__(self):
        opts = self.get_opts()
        for k, v in vars(opts).items():
            varname = 'LOG_' + k.upper()
            default = getattr(self, varname)
            setattr(self, varname, v or default)

    def get_opts(self) -> argparse.Namespace:
        p = argparse.ArgumentParser()
        p.add_argument('-o', '--fname', type=str, default='%s.log' % __name__)
        p.add_argument('-l', '--level', type=str)
        p.add_argument('-s', '--style', type=str)
        p.add_argument('-t', '--trace', action='store_true')
        p.add_argument('-q', '--quiet', action='store_true')
        p.add_argument('-x', '--store', action='store_true')
        p.add_argument('-c', '--cache', action='store_true')
        return p.parse_args()


Settings = Settings()
__all__ = ['Settings']
