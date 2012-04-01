#!/usr/bin/env python
import sys
import os

import siftengine


def test():
    print "OK"
   

class LOGTest(siftengine.SiftEngine):
    def __init__(self):
        siftengine.SiftEngine.__init__(self)
        self.leader = '\.\.(\d+)\: '
        self._found = None
    
    @property
    def name(self):
        return self.__class__
        
    @property
    def found(self):
        return self._found
        
    def on_match(self):
        print "found a match for" , self.__class__
        
    def on_triggered(self):
        print "triggered a sub match for" , self.__class__, self._found
        
    def prepare(self):
        lead = self.leader
        self.add_regex( lead + "Message sequence started initialization. (.+)")
        self.add_regex( lead + "Message sequence two (.+)")
        self.add_regex( lead + "Message sequence three (.+)")
        self.add_regex( lead + "Message sequence four (.+)")
        self.add_regex( lead + "Message sequence initialization five (.+)")
        self._found = 0
        
    def reset(self):
        pass
    
    def parse(self,stream):
            
        while (not stream.at_end) and (not self._matched):
            line = stream.read()
            pattern = self._compiled[self._found].match(line)
            if pattern:
                self._found += 1
                self.on_triggered()
                
                print "-- " , self._found, len(self._compiled)
                
                if self._found == len(self._compiled):
                    self._matched = True
                    self.on_match()
                
            else:
                stream.unread() # back up the pointer to pos before read()
                return
                
    def debug(self):
        print self.__class__, "found", self._found
        
                
                
            
                
            
    
    