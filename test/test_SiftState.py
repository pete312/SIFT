#!python
import unittest
import siftstate
import siftproperty

class MyStateMachine(siftstate.SiftState):
    
    def on_enter(self):
        return "enter"
        
    def on_leave(self):
        return "leave"

     
class TestSiftState(unittest.TestCase):
    
    def setUp(self):
        self.sift_state = MyStateMachine();
        self.traffic_states = ["green","amber","red"]
        self.alert_states = ["good","bad","downright ugly"]
        
    def test1_basic_inheritence(self):
        self.assertTrue( self.sift_state )
        self.assertEqual( siftproperty.version() , self.sift_state.version() )
            
    def test2_register_states(self):
        """assert init_state registers user states"""
        my_states = [1,2,3,4]
        self.sift_state.init_states(my_states)
        
        self.assertEqual(my_states[0], self.sift_state.get_state() )
        
    def test2_unregistered_operations(self):
        """Assert raise exception when state is not initialized"""
        self.failUnlessRaises ( Exception ,self.sift_state.next_state )
        self.failUnlessRaises ( Exception ,self.sift_state.prev_state )
        self.failUnlessRaises ( Exception ,self.sift_state.set_state, "dummy" )
    
    def test3_state_change_to_desired_state(self):
        """Set state to specific state"""
        test_obj = self.sift_state
        test_obj.init_states(self.alert_states)
        self.assertEqual(self.alert_states[0] , test_obj.get_state() )
        
        test_obj.set_state(self.alert_states[2])
        self.assertEqual(self.alert_states[2], test_obj.get_state())
        
    def test4_state_change_up(self):
        """State change from green to amber to red"""
        test_obj = self.sift_state
        test_obj.init_states(self.traffic_states)
        self.assertEqual(self.traffic_states[0] , test_obj.get_state() )
        self.assertEqual(self.traffic_states[1] , test_obj.next_state() ) 
        self.assertEqual(self.traffic_states[1] , test_obj.get_state() )
        self.assertEqual(self.traffic_states[2] , test_obj.next_state() ) 
        self.assertEqual(self.traffic_states[2] , test_obj.get_state() ) 
        

    def test4_state_change_dn(self):
        """State change from bad to good"""
        
        my_states = self.alert_states
        test_obj = self.sift_state
        test_obj.init_states(self.alert_states)
        
        test_obj.set_state(my_states[2])
        self.assertEqual(my_states[2] , test_obj.get_state() )
        self.assertEqual(my_states[1] , test_obj.prev_state() ) 
        self.assertEqual(my_states[1] , test_obj.get_state() )
        self.assertEqual(my_states[0] , test_obj.prev_state() ) 
        self.assertEqual(my_states[0] , test_obj.get_state() )
        

            
        
    def test5_state_change_boundries(self):
        """ Test that Red changes to Green """
        self.assertTrue(False, "TODO: Not yet tested") 
        
    @classmethod
    def state_up_callback():
        pass
        
    @classmethod
    def state_dn_callback():
        pass
    
if __name__ == "__main__":
	unittest.main()