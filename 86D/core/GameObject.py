from dataclasses import dataclass


class _GameObject(type):
    """
    A metaclass which assigns a logger to each `GameObject`.
    """

    def __new__(cls, name, bases, dct):
        """
        Add a `Logger` to any `GameObject` type.
        """
        dct.update({
            '__hash__': _GameObject.__hash__,
            '__eq__': _GameObject.__eq__
        })
        cls = super().__new__(cls, name, bases, dct)
        cls.log = Log.getChild(name)
        cls.count = 0
        return dataclass(repr=False, eq=False)(cls)

    def __hash__(self):
        """
        Default hashing logic.
        """
        return hash((self.__class__, self.count))

    def __eq__(self, other):
        """
        Default equality test compares `hash` values.
        """
        return hash(self) == hash(other)


class GameObject(object, metaclass=_GameObject):

    def __new__(cls, *args, **kwargs):
        """
        Increase the object count upon creation of a new `GameObject`.
        """
        self = super().__new__(cls)
        self.count = cls.count
        self.log = Log.getChild(repr(self))
        if not Settings.LOG_NOGEN:
            self.log.debug('generated.')
        cls.count += 1
        return self

    def __repr__(self):
        """
        Default `repr` logic; i.e. `PlayingCard(0)` represents the first
        generated `PlayingCard`.
        """
        return '%s(%i)' % (self.__class__.__name__, self.count)

    def __str__(self):
        """
        Default `str` logic points to `repr`.
        """
        return repr(self)

    def _assert(self, cond, msg, warn=False):
        """
        Helper function for logging warnings and errors.
        """
        try:
            assert cond, msg
        except AssertionError as e:
            if warn:
                self.log.warning(e, stack_info=Settings.LOG_TRACE)
            else:
                self.log.error(e, stack_info=Settings.LOG_TRACE)
                raise e


__all__ = ['GameObject']
