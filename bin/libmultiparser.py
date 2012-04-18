#!/usr/bin/env python

# this is a lib that demonstrates an expansion of the function of liblogparse.py
# This demonstrates how you can scale up while still maintaining readability.
# Once you get the hang of this you will be writing complex SIFT parsers in no time.

import siftengine
import siftstate

RX_LEADER = '\.\.(\d+)\:\s'
 
class LogBase(siftengine.SiftEngine, siftstate.SiftState):
    def __init__(self, str_name, thread_id, worker):
        siftengine.SiftEngine.__init__(self)
        siftstate.SiftState.__init__(self)
        self.leader = RX_LEADER
        self._found = None
        self._group = []
        self._total_match_count = 0
        self._name = str_name
        self._id = thread_id
        self.worker = worker
        
        #setup state machine green is matched. yellow is in progress of matching, red is not matched or error.
        self.init_states(['red', 'yellow' , 'green']) 
  

    def on_change(self):
        '''Define what to do when state changes.'''
        print " %s changed state from %s to %s" % (self.name , self.last_state(),  self.get_state() )
                
    @property
    def total_match_count(self):
        return self._total_match_count
        
    @property
    def name(self):
        return self._name
        
    @property
    def id(self):
        return self._id
    
    @property
    def found(self):
        return self._found
        
    def on_match(self):
        '''this callback is triggered when an engine becomes fully matched'''
        print "\n ** found a match for %s **\n" % self.name
        
        print "\tinformation gleened from %s:" % self.name
        line = 1
        for group in self._group:
            print "\tline", line, " data  ..", group
            line += 1
        self._total_match_count += 1
        
        # 
        self.set_state(2) # green
        self.worker.set_state( self.id )
        self.reset()
        
    def on_triggered(self,pattern):
        '''this callback is triggered every time a line is found that is a submatch for the engine'''
        
        if self.get_state() == 'green':
            # If here it means that we have started to match again. The state must drop to yellow.
            self.prev_state()
            
        print " %s triggered a sub match for %d of %d" % ( self.name, self._found, len(self._compiled) )
        self._group.append(pattern.groups())
        
        if self.get_state() == "red":
            # already fatal
            return
        
        #change state if message contains fatal
        start_of_fatal_string = pattern.groups()[-1].lower.find('fatal')
        start_of_not_fatal_string = pattern.groups()[-1].lower.find('not fatal')
        if (start_of_fatal_string > 0 
            and start_of_not_fatal_string == 0):
            print "found fatal"
            self.set_state(2)
        else:
            self.set_state(1)
        
    def reset(self):
        '''This is reset for the engine. If not called the parser will never try to rematch anything'''
        self._found = 0
    
                
    def debug(self):
        print self.__class__, "found", self._found
        
T1_THREAD = 1
T2_THREAD = 2 

NOT_READY = 0
T1_READY = 1
T2_READY = 2
READY = 3
    
            
class WorkerPattern(siftengine.SiftEngine, siftstate.SiftState):
    def __init__(self):
        siftengine.SiftEngine.__init__(self)
        siftstate.SiftState.__init__(self)
        self._items = set([])
        self.reset()
        self._name = "worker parser"
        self._error_items = set([])
        
        self.init_states( [NOT_READY, T1_READY, T2_READY, READY] )
        
        print " constructed worker parser"
        
    
    @property
    def name(self):
        return self._name
    
    def reset(self):
        self._state_transitions = set([])
        self._found = 0
        self._matched = False
    
    def on_match(self):
        # on_trigger does all of the work so we just reset the parser so it can match again.
        self.reset()
        
    @property
    def has_error(self):
        return len(self._error_items) > 0
        
    def get_items_in_error(self):
        return self._error_items
        
    def get_completed_items(self):
        return self._items
        
        
    def on_triggered(self, pattern):
        
        # add the item found in this dictionay if the state is ready
        item = pattern.group(2).strip()
        if self.get_state() == READY:
            print "worker processed item \"%s\"" % item
            self._items.add( item )
        else:
            self._error_items.add( item )
            print "Error item \"%s\" encountered before system ready." % ( item )
        
    
    def on_change(self):
        # this callback must reconize that transitions T1_READY and T2_READY 
        # have happened. If true the state transitions into READY
        print " %s changed state from %s to %s" % (self.name , self.last_state(),  self.get_state() )
        self._state_transitions.add(self.get_state())
        
        if self.get_state() == NOT_READY:
            self._state_transitions = set([])
            
        
        if T1_READY in self._state_transitions and T2_READY in self._state_transitions:
            self.set_state(READY)
           
    def prepare(self):
        self.add_regex( RX_LEADER + "worker thread (.+)" )
        self.reset()
        
    
    
    
# factory method to return the porper class.
def ThreadInitSequence(thread, worker):
        
        if type(worker) != WorkerPattern:
            message = "Worker not of type %s found %s instead"  % (WorkerPattern, type(worker))
            raise TypeError(message)

        # factory pattern to pick 
        if thread == T1_THREAD :
            return InitThreadType1(worker)
        elif thread == T2_THREAD:
            return InitThreadType2(worker)
        else:
            namespace = __name__
            err_str = "thread type not < %s.T1_THREAD | %s.T2_THREAD >" % (namespace,namespace)
            raise TypeError(err_str)
            
    
        
class InitThreadType1(LogBase):
    def __init__(self, worker):
        LogBase.__init__(self, "Thread 1 parser", T1_THREAD, worker)
       
        print " constructed %s" % self.name

            
    def prepare(self):
        '''Look for thread 1 message sequence'''
        self.add_regex( RX_LEADER + "thread 1 sequence started initialization. (.+)")
        self.add_regex( RX_LEADER + "thread 1 sequence two (.+)")
        self.add_regex( RX_LEADER + "thread 1 sequence three (.+)")
        self.add_regex( RX_LEADER + "thread 1 sequence four (.+)")
        self.add_regex( RX_LEADER + "thread 1 sequence initialization five (.+)")
        self.reset()

class InitThreadType2(LogBase):
    def __init__(self, worker):
        LogBase.__init__(self, "Thread 2 parser", T2_THREAD, worker)
        
        print " constructed %s" % self.name
    
    def prepare(self):
        '''Look for thread 2 message sequence'''
        self.add_regex( RX_LEADER + "thread 2 initialization start.\s*")
        self.add_regex( RX_LEADER + "thread 2 aquiring socket connection (\d*\.\d*\.\d*\.\d*)\.")
        self.add_regex( RX_LEADER + "thread 2 init complete.")
        self.reset()    
        
    
        
    

