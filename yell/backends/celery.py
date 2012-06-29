from __future__ import absolute_import
from celery.task import Task
from yell import Notification, notify, registry

class CeleryNotificationTask(Task):
    """ Dispatch and run the notification. """
    def run(self, name=None, backend=None, *args, **kwargs):
        """
        The Celery task. 
        
        Delivers the notification via all backends returned by :param:`backend`.
        """
        assert name is not None, "No 'name' specified to notify"
        assert backend is not None, "No 'backend' specified to notify with"
        
        backends = backend().get_backends(*args, **kwargs)
        notify(name, backends=backends, *args, **kwargs)
    
class CeleryNotification(Notification):
    """ 
    Delivers notifications through Celery. 
    
    :example:
    
    ::
    
        from yell import notify, Notification
    
        class EmailNotification(Notification):
            name = 'async'
            def notify(self, *args, **kwargs):
                # Deliver email 
                
        class DBNotification(Notification):
            name = 'async'
            def notify(self, *args, **kwargs):
                # Save to database
        
        class AsyncNotification(CeleryNotification):
            name = 'async'        
        
        notify('async', backends = [AsyncNotification],
            text = "This notification is routed through Celery before being sent and saved")
    
    In the above example when calling :attr:`yell.notify` will invoke ``EmailNotification`` and
    ``DBNotification`` once the task was delivered through Celery.
        
    """
    name = None
    """ 
    The name of this notification. Override in subclasses.
    """
    
    def get_backends(self, *args, **kwargs):
        """
        Return all backends the task should use to deliver notifications.
        By default all backends with the same :attr:`name` except for subclasses
        of :class:`CeleryNotifications` will be used.
        """
        return filter(lambda cls: not isinstance(cls, self.__class__), registry.notifications[self.name])
    
    def notify(self, *args, **kwargs):
        """ 
        Dispatches the notification to Celery
        """
        return CeleryNotificationTask.delay(name=self.name, backend=self.__class__, *args, **kwargs)


