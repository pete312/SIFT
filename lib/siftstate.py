import siftproperty

class SiftState(object):

    def __init__(self):
        self._states = []
        self._current_state = None

    def version(self):
        return siftproperty.version()
       
    def onEnter(self, context):
        pass
        
    def init_states(self, state_list ):
        self._states = state_list
        self._current_state = 0

    def get_state(self):
        return self._states[self._current_state]
        
    def del_state(self):
        del self._states
        
    state = property(get_state, init_states, del_state, "State register.")