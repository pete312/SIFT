#!python
import unittest
import siftdata
import siftproperty


class TestSiftData(unittest.TestCase):

    def setUp(self):
        self.sift_data = SiftData();
        self.traffic_data = ["green","amber","red"]

        
    def test1_basics(self):
        """standard class function tests"""
        self.assertTrue( self.sift_data )
        self.assertEqual( siftproperty.version() , SiftData.version() )
        
        
    def test2_read_write_functions(self):
        """test that the basic store and retrieve works"""
        test_obj = self.sift_data
        data = self.traffic_data
        

        test_obj.store(data[0], False):
        test_obj.store(data[1], True):
        test_obj.store(data[2], False):
        
        # peek(position) looks at 
        self.assertTrue( self.test_obj.peek(1) )
        
        
        
    