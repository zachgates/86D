from dataclasses import dataclass


class _GameObject(type):
    """
    A metaclass which assigns a logger to each `GameObject`.
    """

    _count = 0

    def __new__(cls, name, bases, dct):
        """
        Add a `Logger` to any `GameObject` type.
        """
        dct.update({
            '__hash__': _GameObject.__hash__,
            '__eq__': _GameObject.__eq__,
            '__repr__': _GameObject.__repr__,
        })
        cls = type.__new__(cls, name, bases, dct)
        cls = dataclass(cls)
        cls.log = LOG.getChild(name)
        return cls

    def __call__(cls, *args, **kwargs):
        _GameObject._count += 1
        self = type.__call__(cls, *args, **kwargs)
        self._id = hex(_GameObject._count)
        self.log = LOG.getChild(repr(self))
        if APP.SETTINGS.LOG_TRACK:
            self.log.debug('generated.')
        return self

    def __hash__(self):
        return int(self._id, 16)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self._id)


class GameObject(object, metaclass=_GameObject):

    _id = hex(0)

    def __str__(self):
        return repr(self)

    def _assert(self, cond, msg, warn=False):
        try:
            assert cond, msg
        except AssertionError as e:
            if warn:
                self.log.warning(e, stack_info=APP.SETTINGS.LOG_TRACE)
            else:
                self.log.error(e, stack_info=APP.SETTINGS.LOG_TRACE)
                raise e


__all__ = ['GameObject']
