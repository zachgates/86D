import logging


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


class GameObject(object, metaclass=__GameObject):

    count = 0

    def __new__(cls, *args, **kwargs):
        """
        Increase the object count upon creation of a new `GameObject`.
        """
        self = super().__new__(cls)
        self.count = cls.count
        self.log = self.log.getChild(repr(self))
        self.log.debug('generated')
        cls.count += 1
        return self

    def __hash__(self):
        return hash((self.__class__, self.count))

    def __repr__(self):
        return '%s(%i)' % (self.__class__.__name__, self.count)

    def __str__(self):
        return repr(self)


__all__ = ['GameObject']
