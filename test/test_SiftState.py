#!python
import unittest
import siftstate
import siftproperty

class MyStateMachine(siftstate.SiftState):
    
    def onEnter(self):
        return True
        
    def onLeave(self):
        return True

     
class TestSiftState(unittest.TestCase):
    
    def setUp(self):
        self.sift_state = MyStateMachine();
        self.traffic_states = ["green","amber","red"]
        self.alert_states = ["good","bad","downright ugly"]
        
    def test_basic_inheritence(self):
        self.assertTrue( self.sift_state )
        self.assertEqual( siftproperty.version() , self.sift_state.version() )
            
    def test_register_states(self):
        my_states = [1,2,3,4]
        self.sift_state.init_states(my_states)
        
        self.assertEqual(my_states[0] , self.sift_state.get_state() )
        
    def test_state_change_up(self):
        test_obj = self.sift_state
        test_obj.init_states(self.traffic_states)
        
    def test_state_change_dn(self):
        test_obj = self.sift_state
        test_obj.init_states(self.traffic_states)
        
    @classmethod
    def state_up_callback():
        pass
        
    @classmethod
    def state_dn_callback():
        pass
    
if __name__ == "__main__":
	unittest.main()