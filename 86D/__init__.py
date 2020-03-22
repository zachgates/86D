from .settings import SETTINGS


LOG = __import__('logging').getLogger(__name__)


__all__ = ['SETTINGS', 'LOG']
