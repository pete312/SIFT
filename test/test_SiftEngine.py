#!/usr/bin/python
import unittest


class TestHelper(SiftEngine):
    def __init__(self):
        pass
        
    def IsConstructed(self):
        return true
        
        


class TestSiftEngine(unittest.TestCase):
    
    def SetUp():
        self.sift_engine = TestHelper();
    
    def test_Inherit_and_instantiate():
        self.assertIsTrue(self.sift_engine.IsConstructed)
        
    def test_Sift_engine_finds_test_string():
        pass
    
    
    
if __name__ == "__main__":
	unittest.main()
    