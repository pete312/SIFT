import siftproperty
import abc

class SiftState(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._states = []
        self._current_state = None
        self._last_state = None
        self._roll_at_top_state = False
        self._roll_at_bottom_state = False

    @staticmethod
    def version():
        return siftproperty.version()
        
    def next_state(self):

        if self._current_state == None:
            raise Exception("Uninitialized", "State not initialized")
        
        
        self._last_state = self._current_state
        if self._current_state < len(self._states) - 1:
            self._current_state += 1
        else:
            if self._roll_at_top_state:
                self._current_state = 0
             
        return self._states[self._current_state]
                
                
    def prev_state(self):
        if self._current_state == None:
            raise Exception("Uninitialized", "State not initialized")
            
        self._last_state = self._current_state    
        if self._current_state > 0:
            self._current_state -= 1
        else:
            if self._roll_at_bottom_state:
                self._current_state = len(self._states) -1
        
        return self._states[self._current_state]
       
    @abc.abstractmethod
    def on_change(self):
        pass
    
    def set_state(self, desired_state=0):
        """set to desired state: returns success or fail or raise if not ready"""
        if self._current_state == None:
            raise Exception("Uninitialized", "State not initialized")
        
        if desired_state >= len(self._states)  and desired_state < 0:
            raise IndexError("state out of bounds")
             
        self._states[desired_state]
        self._last_state = self._current_state
        self._current_state = desired_state
        if self._last_state != desired_state:
            self.on_change()
        return True
        
    def init_states(self, state_list ):
        self._states = state_list
        self._current_state = 0
        self._last_state = 0

    def get_state(self):
        return self._states[self._current_state]
        
    def last_state(self):
        return self._states[self._last_state]
    
    def del_state(self):
        del self._states
        self._current_state = None
        
        
    def roll_at_top_state(self, bool):
        """Decide if top state rolls to bottom state"""
        self._roll_at_top_state = bool
        
    def roll_at_bottom_state(self, bool):
        """Decide if top state rolls to bottom state"""
        self._roll_at_bottom_state = bool
        
    states = property(get_state, init_states, del_state, "State register.")
    
    