from yell import Notification, notify

class DecoratedNotification(Notification):
    func = None
    """
    The function that has been decorated. 
    """

    def notify(self, *args, **kwargs):
        return self.func(*args, **kwargs)

def notification(name=None, backends=None):
    """
    Decorator to simplify creation of notification backends. 
    
    :example:
    
    ::
    
        from yell.decorators import notification
        from yell import notify 
    
        @notification('like')
        def like_email(user, obj):
            send_mail("%s liked %s" % (user, obj), "No/Text", "noreply@example.com",
                [obj.user.email])
        
        @notification('like')
        def like_db(user, obj):
            DBNotification.objects.create(user = user, obj = obj, type = 'like')
    
        @notification('like')
        def like(*args, **kwargs):
            pass
        
        # Use all backends
        notify('like', user = user, obj = obj)        
        like.notify(user = user, obj = obj)
        
        # Only use the email backend
        like_email.notify_once(user = user, obj = obj)
        
    """

    def wrapper(func):
        def funcwrapper(self, *args, **kwargs):
            """ Wrapping the notification function so it doesn't receive `self` """
            return func(*args, **kwargs)
        
        NotificationCls = type('%sNotification' % name.lower().title(), (DecoratedNotification,), {
            'func': funcwrapper,
            'name': name
        })

        def notify_all(*args, **kwargs):
            """
            Sends this notification off to every backend with the configured name. 
            """
            return notify(name, *args, **kwargs)
        
        def notify_once(*args, **kwargs):
            """
            Sends this notification off only to the current backend.
            """
            return notify(name, backends=[NotificationCls], *args, **kwargs)
        
        func.notify = notify_all
        func.notify_once = notify_once
        
        return func
        
    return wrapper
