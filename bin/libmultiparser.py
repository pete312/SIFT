#!/usr/bin/env python

# this is a lib that demonstrates an expansion of the function of liblogparse.py
# This demonstrates how you can scale up while still maintaining readability.
# Once you get the hang of this you will be writing complex SIFT parsers in no time.

import siftengine
import siftstate

RX_LEADER = '\.\.(\d+)\: '
 
class LogBase(siftengine.SiftEngine, siftstate.SiftState):
    def __init__(self):
        siftengine.SiftEngine.__init__(self)
        siftstate.SiftState.__init__(self)
        self.leader = RX_LEADER
        self._found = None
        self._group = []
        self._total_match_count = 0
        
        #setup state machine
        self.init_states(['red', 'yellow' , 'green']) 
        print self.get_state()

    def on_change(self):
        '''Define what to do when state changes.'''
        print "state change from", self.last_state(), "to" , self.get_state()
                
    @property
    def total_match_count(self):
        return self._total_match_count
    
    @property
    def name(self):
        return self.__class__
        
    @property
    def found(self):
        return self._found
        
    def on_match(self):
        '''this callback is triggered when an engine becomes fully matched'''
        print "found a match for" , self.__class__
        
        print "information gleened from the parse was:"
        line = 1
        for group in self._group:
            print "line", line, " data  ..", group
            line += 1
        self._total_match_count += 1
        
        # so now what state should this engine be in. Lets say its red
        self.set_state(2)
        self.reset()
        
    def on_triggered(self,pattern):
        '''this callback is triggered every time a line is found that is a submatch for the engine'''
        print "triggered a sub match for" , self.__class__, self._found, "of" , len(self._compiled)
        self._group.append(pattern.groups())
        
        if self.get_state() == "red":
            # already fatal
            return
        
        #change state if message contains fatal
        start_of_fatal_string = pattern.groups()[-1].find('fatal')
        start_of_not_fatal_string = pattern.groups()[-1].find('not fatal')
        if (start_of_fatal_string > 0 
            and start_of_not_fatal_string == 0):
            print "found fatal"
            self.set_state(2)
        else:
            self.set_state(1)
        
    def reset(self):
        '''This is reset for the engine. If not called the parser will never try to rematch anything'''
        self._found = 0
        self._matched = False
        
        # In the reset we can decide to reset the state to undefined
    
                
    def debug(self):
        print self.__class__, "found", self._found
    

NOT_READY = 0
T1_READY = 1
T2_READY = 2
READY = 4
    
            
class WorkerPattern(siftengine.SiftEngine, siftstate.SiftState):
    def __init__(self):
        siftengine.SiftEngine.__init__(self)
        siftstate.SiftState.__init__(self)
        self._items = set([])
        self.leader = RX_LEADER
        self.reset()
        
        
        self.init_states([NOT_READY, T1_READY, T2_READY, READY])
    
    @property
    def name(self):
        return self.__class__
    
    def reset(self):
        self._state_transitions = set([])
    
    def on_match(self):
        pass
        
    def on_triggered(self, pattern):
        
        # add the item found in this dictionay if the state is ready
        if self.get_state() == READY:
            self._items.add( pattern.group()[0] )
        else:
            print "Item %s encountered before system ready." % pattern.group()[0]
        
    
    def on_change(self):
        # this callback must reconize that transitions T1_READY and T2_READY 
        # have happened. If true the state transitions into READY
        self._state_transitions.add(self.get_state())
        
        if self.get_state() == NOT_READY:
            self._state_transitions = set([])
        
        if T1_READY and T2_READY in self._state_transitions:
            self.set_state(READY)
           
    def prepare(self):
        lead = self.leader
        self.add_regex( lead + "Autonomus message (.+)" )
        self.reset()
    
    
# factory method to return the porper class.
def ThreadInitSequence(thread, worker):
        
        if type(worker) != WorkerPattern:
            message = "Worker not of type %s found %s instead"  % (WorkerPattern, type(worker))
            raise TypeError(message)

        # factory pattern to pick 
        if thread == 1 :
            return InitThreadType1()
        elif thread == 2:
            return InitThreadType2()
        else:
            raise TypeError("thread type not <1|2>")
            
    
        
class InitThreadType1(LogBase):
    def __init__(self):
        LogBase.__init__(self)
            
    def prepare(self):
        '''Look for thread 1 message sequence'''
        self.add_regex( RX_LEADER + "Message sequence started initialization. (.+)")
        self.add_regex( RX_LEADER + "Message sequence two (.+)")
        self.add_regex( RX_LEADER + "Message sequence three (.+)")
        self.add_regex( RX_LEADER + "Message sequence four (.+)")
        self.add_regex( RX_LEADER + "Message sequence initialization five (.+)")
        self.reset()

class InitThreadType2(LogBase):
    def __init__(self):
        LogBase.__init__(self)
    
    def prepare(self):
        '''Look for thread 2 message sequence'''
        self.add_regex( RX_LEADER + "thread 2 initialization start.\s*")
        self.add_regex( RX_LEADER + "thread 2 warming up.")
        self.add_regex( RX_LEADER + "thread 2 init complete.")
        self.reset()    
        
    
        
    

