#!/usr/bin/env python

# this is a lib for sift.py. look at sift.py for usage of this lib.

import siftengine
import siftstate


class LOGTest(siftengine.SiftEngine, siftstate.SiftState):
    def __init__(self):
        siftengine.SiftEngine.__init__(self)
        siftstate.SiftState.__init__(self)
        self.leader = '\.\.(\d+)\: '
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
        self.set_state(2)
        self.reset()
        
    def on_triggered(self,pattern):
        '''this callback is triggered every time a line is found that is a submatch for the engine'''
        print "triggered a sub match for" , self.__class__, self._found, "of" , len(self._compiled)
        self._group.append(pattern.groups())
        
        #change state if message contains fatal
        start_of_fatal_string = pattern.groups()[-1].find('fatal')
        start_of_not_fatal_string = pattern.groups()[-1].find('not fatal')
        if (start_of_fatal_string > 0 
            and start_of_not_fatal_string == 0):
            print "found fatal"
        else:
            self.set_state(1)
            
        
        
    def prepare(self):
        '''User must enter the expressions that decribe the paragraph this engine is looking for'''
        lead = self.leader
        self.add_regex( lead + "Message sequence started initialization. (.+)")
        self.add_regex( lead + "Message sequence two (.+)")
        self.add_regex( lead + "Message sequence three (.+)")
        self.add_regex( lead + "Message sequence four (.+)")
        self.add_regex( lead + "Message sequence initialization five (.+)")
        self.reset()
        
    def reset(self):
        '''This is reset for the engine. If not called the parser will never try to rematch anything'''
        self._found = 0
    
                
    def debug(self):
        print self.__class__, "found", self._found
        
                
                
            
                
            
    
  