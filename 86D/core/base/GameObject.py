import logging

from dataclasses import dataclass

from ... import LOG_TRACE


def gameclass(cls):
    return dataclass(repr=False, eq=False)(cls)


class __GameObject(type):
    """
    A metaclass which assigns a logger to each `GameObject`.
    """

    def __new__(cls, name, bases, dct):
        """
        Add a `Logger` to any `GameObject` type.
        """
        cls = super().__new__(cls, name, bases, dct)
        cls.log = logging.getLogger(name)
        cls.count = 0
        return cls


@gameclass
class GameObject(object, metaclass=__GameObject):

    def __new__(cls, *args, **kwargs):
        """
        Increase the object count upon creation of a new `GameObject`.
        """
        self = super().__new__(cls)
        self.count = cls.count
        self.log = logging.getLogger().getChild(repr(self))
        self.log.debug('generated.')
        cls.count += 1
        return self

    def __hash__(self):
        return hash((self.__class__, self.count))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return '%s(%i)' % (self.__class__.__name__, self.count)

    def __str__(self):
        return repr(self)

    def _assert(self, cond, msg, warn=False):
        try:
            assert cond, msg
        except AssertionError as e:
            if warn:
                self.log.warning(e, stack_info=LOG_TRACE)
            else:
                self.log.error(e, stack_info=LOG_TRACE)


__all__ = ['gameclass', 'GameObject']
