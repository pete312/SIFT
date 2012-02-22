import siftproperty
import abc

class SiftState(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._states = []
        self._current_state = None
        self._reset_at_top_state = False

    def version(self):
        return siftproperty.version()
        
    def next_state(self):
        if self._current_state == None:
            raise Exception("Uninitialized", "State not initialized")
            
        if self._current_state < len(self._states):
            self._current_state += 1
        else:
            if self._reset_at_top_state:
                self._current_state = 0
        return self._states[self._current_state]
                
                
    def prev_state(self):
        if self._current_state == None:
            raise Exception("Uninitialized", "State not initialized")
            
        if self._current_state > len(self._states):
            self._current_state += 1
        else:
            if self._reset_at_top_state:
                self._current_state = 0
        return self._states[self._current_state]
       
       
    @abc.abstractmethod
    def on_enter(self):
        pass
        
    @abc.abstractmethod
    def on_leave(self):
        pass
    
    def set_state(self, desired_state):
        """set to desired state"""
        if self._current_state == None:
            raise Exception("Uninitialized", "State not initialized")
        
    def init_states(self, state_list ):
        self._states = state_list
        self._current_state = 0

    def get_state(self):
        return self._states[self._current_state]
        
    def del_state(self):
        del self._states
        self._current_state = None
        
    state = property(get_state, init_states, del_state, "State register.")