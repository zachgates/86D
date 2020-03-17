import logging


class __GameObject(type):
    """
    A metaclass which assigns a logger to each `GameObject`.
    """

    def __new__(cls, name, bases, dct):
        """
        Add a `Logger` to any `GameObject` type.
        """
        obj = super().__new__(cls, name, bases, dct)
        obj.log = logging.getLogger(name)
        obj.count = 0
        return obj


class GameObject(object, metaclass=__GameObject):

    count = 0

    def __new__(cls, *args, **kwargs):
        """
        Increase the object count upon creation of a new `GameObject`.
        """
        obj = super().__new__(cls)
        obj.count = cls.count
        obj.log = cls.log.getChild(str(obj.count))
        obj.log.debug('generated')
        cls.count += 1
        return obj


__all__ = ['GameObject']
