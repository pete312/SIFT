#!/usr/bin/env python
import unittest
import sys
from os.path import dirname, normpath, join, abspath

basedir = dirname(abspath(sys.argv[0]))
libpath = normpath(join(basedir, "../lib"))
sys.path.append(libpath)

import siftdata
import siftproperty


class TestSiftData(unittest.TestCase):

    def setUp(self):
        self.sift_data = siftdata.SiftData();
        self.traffic_data = ["green","amber","red"]

        
    def test0_construct(self):
        """standard class function tests"""
        self.assertTrue( self.sift_data )
        self.assertEqual( siftdata.SiftData.version() , siftproperty.version() )
        
        
    def test2_read_write_functions(self):
        """test store and peek """
        test_obj = self.sift_data
        data = self.traffic_data
       
        test_obj.store(data[0], False)
        test_obj.store(data[1], True)
        test_obj.store(data[2], False)
        
        # peek(position) looks at 
        self.assertTrue( test_obj.peek(data[1]) )
        
        
    def test3_push_and_pop(self):
        """Test for push and pop"""
        test_obj = self.sift_data
        test_obj.push_back(5)
        test_obj.push_back(4)
        test_obj.push_back(3)
        
        self.assertEqual(test_obj.pop_back(), 3 )
        self.assertEqual(test_obj.pop_front(), 5 )
        self.assertEqual(test_obj.pop_back(), 4 )
    
    def test4_empty_tests(self):
        """Tests for empty set"""
        test_obj = self.sift_data
        
        self.failUnlessRaises(siftdata.Empty, test_obj.peek, 4 )
        self.failUnlessRaises(siftdata.Empty, test_obj.pop_front)
        self.failUnlessRaises(siftdata.Empty, test_obj.pop_back )
         
        
if __name__ == "__main__":
    unittest.main()