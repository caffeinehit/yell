from __future__ import absolute_import
from celery.task import Task
from yell import Yell, yell, registry

class CeleryYellingTask(Task):
    """ Dispatch and run the yelling """
    def run(self, name=None, yeller=None, *args, **kwargs):
        """
        The Celery task. 
        
        Delivers the notification via all backends returned by :param:`yeller`.
        """
        assert name is not None, "No 'name' specified to yell"
        assert yeller is not None, "No 'yeller' specified to yell with"
        
        backends = yeller().get_backends(*args, **kwargs)
        yell(name, backends=backends, *args, **kwargs)
    
class CeleryYell(Yell):
    """ 
    Delivers notifications through Celery. 
    
    :example:
    
    ::
    
        from yell import yell, Yell
    
        class EmailYell(Yell):
            yell = 'async'
            def yell(self, *args, **kwargs):
                # Deliver email 
                
        class DBYell(Yell):
            yell = 'async'
            def yell(self, *args, **kwargs):
                # Save to database
        
        class AsyncYell(CeleryYell):
            yell = 'async'        
        
        yell('async', backends = [AsyncYell],
            text = "This notification is routed through Celery before being sent and saved")
    
    In the above example when calling :attr:`yell.yell` will invoke ``EmailYell`` and
    ``DBYell`` once the task was delivered through Celery.
        
    """
    name = None
    """ 
    The name of this notification. Override in subclasses.
    """
    
    def get_backends(self, *args, **kwargs):
        """
        Return all backends the task should use to deliver notifications.
        By default all backends with the same :attr:`name` except for subclasses
        of :class:`CeleryYell` will be used.
        """
        return filter(lambda cls: not isinstance(cls, self.__class__), registry.yells[self.yell])
    
    def yell(self, *args, **kwargs):
        """ 
        Dispatches the notification to Celery
        """
        return CeleryYellingTask.delay(name=self.name, yeller=self.__class__, *args, **kwargs)


