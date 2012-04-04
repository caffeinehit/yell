from yell import Yell, yell

class DecoratedYell(Yell):
    func = None
    """
    The function that has been decorated. 
    """

    def yell(self, *args, **kwargs):
        return self.func(*args, **kwargs)

def yelling(name=None, backends=None):
    """
    Decorator to simplify creation of notification backends. 
    
    :example:
    
    ::
    
        from yell.decorators import notification
        from yell import yell 
    
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
        yell('like', user = user, obj = obj)        
        like.yell(user = user, obj = obj)
        
        # Only use the email backend
        like_email.yell_once(user = user, obj = obj)
        
    """

    def wrapper(func):
        def funcwrapper(self, *args, **kwargs):
            """ Wrapping the yelling function so it doesn't receive `self` """
            return func(*args, **kwargs)
        
        YellCls = type('%sYell' % name.lower().title(), (DecoratedYell,), {
            'func': funcwrapper,
            'name': name
        })

        def yell_all(*args, **kwargs):
            """
            Sends this yell off to every backend with the configured name. 
            """
            return yell(name, *args, **kwargs)
        
        def yell_once(*args, **kwargs):
            """
            Sends this yell off only to the current backend.
            """
            return yell(name, backends=[YellCls], *args, **kwargs)
        
        func.yell = yell_all
        func.yell_once = yell_once
        
        return func
        
    return wrapper
