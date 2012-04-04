__version__ = "0.1"

import registry

class MetaYell(type):
    """ 
    Metaclass that stores all yells in the registry.
    """
    def __new__(cls, name, bases, attrs):
        Yell = super(MetaYell, cls).__new__(cls, name, bases, attrs)

        if Yell.name is not None:
            registry.yells[Yell.name] = registry.yells.get(Yell.name, []) + [Yell]

        return Yell


class Yell(object):
    """
    Base class for any kind of notifications. Inherit from this class to create
    your own notification types and backends. 
    
    Subclasses need to implement :meth:`yell`.
    """
    __metaclass__ = MetaYell

    name = None
    """
    A name for this yell.
    """
    
    def yell(self, *args, **kwargs):
        """
        A method that delivers a notification.
        """
        raise NotImplementedError

def yell(name, *args, **kwargs):
    """
    Send notifications. If ``backends==None``, all backends with the same name
    will be used to deliver a notification. 
    
    If ``backends`` is a list, only the specified backends will be used.
    
    :param name: The yell to send
    :param backends: A list of backends to be used or ``None`` to use all associated backends
    """
    assert name in registry.yells, "'{0}' is not a valid yell.".format(repr(name))
    
    backends = kwargs.pop('backends', None)
    
    if backends is None:
        backends = registry.yells[name]
    
    results = []

    for Backend in backends:
        backend = Backend()
        results.append(backend.yell(*args, **kwargs))
    
    return results


