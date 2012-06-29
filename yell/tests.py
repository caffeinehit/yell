from yell import notify, Notification
from yell.decorators import notification


try:
    import unittest2 as unittest
except ImportError:
    import unittest
    
@notification(name='decorator')
def decorator_notification0(*args, **kwargs):
    return 'Decorator 0', args, kwargs

@notification(name='decorator')
def decorator_notification1(*args, **kwargs):
    return 'Decorator 1', args, kwargs

class ClassNotification0(Notification):
    name = 'class'
    
    def notify(self, *args, **kwargs):
        return 'Class 0', args, kwargs

class ClassNotification1(Notification):
    name = 'class'
    
    def notify(self, *args, **kwargs):
        return 'Class 1', args, kwargs

class AssertMixin(object):
    retval = None
    def _assert_results(self, results):
        for i, result in enumerate(results):
            self.assertTrue('%s %s' % (self.retval, i) == result[0], """ Return value '%s %s' not equal to '%s' """ % (self.retval, i, result[0]))

            self.assertTrue('Arg1' == result[1][0], """ Expected value 'Arg1' does not match received value '%s' """ % result[1][0])
            self.assertTrue('Arg2' == result[1][1], """ Expected value 'Arg2' does not match received value '%s' """ % result[1][1])
            
            self.assertTrue('Kwarg1' in result[2].values())
            self.assertTrue('Kwarg2' in result[2].values())
            

class TestDecoratorNotification(AssertMixin, unittest.TestCase):
    retval = 'Decorator'

    def test_notifying_with_decorator(self):
        results = notify('decorator', 'Arg1', 'Arg2', kwarg1='Kwarg1', kwarg2='Kwarg2')
        self.assertEqual(2, len(results))           
        self._assert_results(results)

        results = decorator_notification0.notify('Arg1', 'Arg2', kwarg1='Kwarg1', kwarg2='Kwarg2')
        self._assert_results(results)
        self.assertEqual(2, len(results))           
    

    def test_notifying_once_with_decorator(self):
        results = decorator_notification0.notify_once('Arg1', 'Arg2', kwarg1='Kwarg1', kwarg2='Kwarg2')
        self.assertEqual(1, len(results))
        self._assert_results(results)


class TestClassNotification(AssertMixin, unittest.TestCase):
    retval = 'Class'
    
    def test_notifying_with_class(self):
        results = notify('class', 'Arg1', 'Arg2', kwarg1='Kwarg1', kwarg2='Kwarg2')
        self.assertEqual(2, len(results))           
        self._assert_results(results)

    def test_notifying_once_with_class(self):
        results = notify('class', 'Arg1', 'Arg2', kwarg1='Kwarg1', kwarg2='Kwarg2', backends=[ClassNotification0])
        self.assertEqual(1, len(results))
        self._assert_results(results)


