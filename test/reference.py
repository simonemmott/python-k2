import unittest
from unittest import TestCase

from k2.reference import reference, RefItem

@reference('reference')
class Example(RefItem):
    def __init__(self, **kw):
        for key, value in kw.items():
            setattr(self, key, value)


class RefItemTest(TestCase):
    
    def reference_test(self):
        
        ex = Example(reference='ref1')
        self.assertEqual('ref1', ex.__ref__())
        self.assertEqual('ref1', str(ex))
    
    def repr_test(self):
        
        ex = Example(reference='ref1')
        self.assertEqual('ref1', str(ex))
    
        
if __name__ == '__main__':
    unittest.main()