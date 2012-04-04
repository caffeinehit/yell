====
yell
====

Pluggable notifications for your Python apps. 

`yell` is not a notification storage or delivery backend but a set of APIs that make it easy to add your own delivery mechanisms.


Using yelling decorators
------------------------

::

    from yell.decorators import yelling
    
    @yelling(name = 'buffalo')
    def buffalo_printer(message):
        print message
    
    @yelling(name = 'buffalo')
    def buffalo_saver(message):
        save(message)
        
    yell("buffalo", _("Buffalo buffalo Buffalo buffalo buffalo buffalo Buffalo buffalo"))


Using yelling classes
---------------------

:: 

    from yell import Yell, yell

    class Buffalo(Yell):
        name = "buffalo"
        message = _("Buffalo buffalo Buffalo buffalo buffalo buffalo Buffalo buffalo")
        
        def yell(self, *args, **kwargs):
            print self.message
        
    class BuffaloEmail(Buffalo):
        def yell(self, *args, **kwargs):
            send_mail("Buffalo", self.message, 'buffalo@example.com', [kwargs.get('user').email])

    class BuffaloDatabase(Buffalo):
        def yell(self, *args, **kwargs):
            BuffaloModel.objects.create(user = kwargs.get('user'))

    # The default behaviour is to use every notification backend with the same 
    # name 
    yell("buffalo", user = User.objects.get(id=1))

    # Only send emails
    yell("buffalo", user = User.objects.get(id=1), backends = [BuffaloEmail])
