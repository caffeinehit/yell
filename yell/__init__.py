__version__ = "0.2"

import registry

class MetaNotification(type):
    """ 
    Metaclass that stores all notifications in the registry.
    """
    def __new__(cls, name, bases, attrs):
        Notification = super(MetaNotification, cls).__new__(cls, name, bases, attrs)

        if Notification.name is not None:
            registry.notifications[Notification.name] = registry.notifications.get(Notification.name, []) + [Notification]

        return Notification


class Notification(object):
    """
    Base class for any kind of notifications. Inherit from this class to create
    your own notification types and backends. 
    
    Subclasses need to implement :meth:`notify`.
    """
    __metaclass__ = MetaNotification

    name = None
    """
    A name for this notification.
    """
    
    def notify(self, *args, **kwargs):
        """
        A method that delivers a notification.
        """
        raise NotImplementedError

def notify(name, *args, **kwargs):
    """
    Send notifications. If ``backends==None``, all backends with the same name
    will be used to deliver a notification. 
    
    If ``backends`` is a list, only the specified backends will be used.
    
    :param name: The notification to send
    :param backends: A list of backends to be used or ``None`` to use all associated backends
    """
    assert name in registry.notifications, "'{0}' is not a valid notification.".format(repr(name))
    
    backends = kwargs.pop('backends', None)
    
    if backends is None:
        backends = registry.notifications[name]
    
    results = []

    for Backend in backends:
        backend = Backend()
        results.append(backend.notify(*args, **kwargs))
    
    return results


