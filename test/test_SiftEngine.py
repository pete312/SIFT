#!python
import unittest
import siftengine
import siftproperty


class TestHelper(siftengine.SiftEngine):
    def __init__(self):
        pass
        
    def is_constructed(self):
        return True
        
     
     
class TestSiftEngine(unittest.TestCase):
    
    def setUp(self):
        self.sift_engine = TestHelper();
    
    def test_inherit_and_instantiate(self):
        self.assertTrue( self.sift_engine )
        self.assertEqual( siftproperty.version(), self.sift_engine.version() )
        
    def test_sift_engine_finds_test_string(self):
        pass
    
    
    
if __name__ == "__main__":
	unittest.main()
    