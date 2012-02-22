#!python
import unittest
import siftstate
import siftproperty

     
class TestSiftState(unittest.TestCase):
    
    def setUp(self):
        self.sift_state = siftstate.SiftState();
        
    def test_basic_inheritence(self):
        self.assertTrue( self.sift_state )
        self.assertEqual( siftproperty.version() , self.sift_state.version() )
            
    def test_register_states(self):
        my_states = [1,2,3,4]
        self.sift_state.init_states(my_states)
        
        self.assertEqual(my_states[0] , self.sift_state.get_state() )

        
    
    
if __name__ == "__main__":
	unittest.main()