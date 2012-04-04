from yell import yell, Yell
from yell.decorators import yelling


try:
    import unittest2 as unittest
except ImportError:
    import unittest
    
@yelling(name='decorator')
def decorator_yell0(*args, **kwargs):
    return 'Decorator 0', args, kwargs

@yelling(name='decorator')
def decorator_yell1(*args, **kwargs):
    return 'Decorator 1', args, kwargs

class ClassYell0(Yell):
    name = 'class'
    
    def yell(self, *args, **kwargs):
        return 'Class 0', args, kwargs

class ClassYell1(Yell):
    name = 'class'
    
    def yell(self, *args, **kwargs):
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
            

class TestDecoratorYell(AssertMixin, unittest.TestCase):
    retval = 'Decorator'

    def test_yelling_with_decorator(self):
        results = yell('decorator', 'Arg1', 'Arg2', kwarg1='Kwarg1', kwarg2='Kwarg2')
        self.assertEqual(2, len(results))           
        self._assert_results(results)

        results = decorator_yell0.yell('Arg1', 'Arg2', kwarg1='Kwarg1', kwarg2='Kwarg2')
        self._assert_results(results)
        self.assertEqual(2, len(results))           
    

    def test_yelling_once_with_decorator(self):
        results = decorator_yell0.yell_once('Arg1', 'Arg2', kwarg1='Kwarg1', kwarg2='Kwarg2')
        self.assertEqual(1, len(results))
        self._assert_results(results)


class TestClassYell(AssertMixin, unittest.TestCase):
    retval = 'Class'
    
    def test_yelling_with_class(self):
        results = yell('class', 'Arg1', 'Arg2', kwarg1='Kwarg1', kwarg2='Kwarg2')
        self.assertEqual(2, len(results))           
        self._assert_results(results)

    def test_yelling_once_with_class(self):
        results = yell('class', 'Arg1', 'Arg2', kwarg1='Kwarg1', kwarg2='Kwarg2', backends=[ClassYell0])
        self.assertEqual(1, len(results))
        self._assert_results(results)


