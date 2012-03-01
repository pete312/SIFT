#!/usr/bin/env python
import unittest
import siftengine
import siftproperty
import siftstate


class TestHelper(siftengine.SiftEngine, siftstate.SiftState):
    def __init__(self):
        siftengine.SiftEngine.__init__(self)
        siftstate.SiftState.__init__(self)
    
        self._expressions = ['dummy']
    
    @property
    def expressions(self):
        return self._expressions
        
    def prepare(self):
        self.add_regex("regex one")
        self.add_regex("regex two")
        return True

    def reset(self):
        return True
        
    def on_match(self):
        return True
        
    def on_triggered(self):
        return True
    
    def on_leave(self):
        pass
        
    def on_enter(self):
        pass
        
     
     
class TestSiftEngine(unittest.TestCase):
    
    def setUp(self):
        self.sift_engine = TestHelper();
    
    def test0_construction(self):
        self.assertTrue( self.sift_engine )
        self.assertEqual( siftproperty.version(), self.sift_engine.version() )
        
    def test1_add_expression(self):
        test_obj = self.sift_engine
        test_obj.prepare()
        empty = TestHelper()
        self.assertEqual(['dummy','regex one', 'regex two'], test_obj.get_segment() )
        self.assertEqual( ['dummy'], empty.get_segment() )
    
    
if __name__ == "__main__":
	unittest.main()
    