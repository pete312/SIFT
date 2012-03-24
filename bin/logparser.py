#!/usr/bin/env python
import sys
import os

import siftengine


def test():
    print "OK"

class LOGTest(siftengine.SiftEngine):
    def __init__(self):
        siftengine.SiftEngine.__init__(self)
        self._expressions = []
        self.leader = '\.\.(\d+)\:'
        
    @property
    def expressions(self):
        return self._expressions
        
    def on_match(self):
        pass
        
    def on_triggered(self):
        pass
        
    def prepare(self):
        lead = self.leader
        self.add_regex( lead + "Message sequence started initialization. (.+)")
        self.add_regex( lead + "Message sequence two (.+)")
        self.add_regex( lead + "Message sequence three (.+)")
        self.add_regex( lead + "Message sequence four (.+)")
        self.add_regex( lead + "Message sequence initialization five (.+)")
        
    def reset(self):
        pass
    
    def parse(self,stream):
        at_end = False
        # TODO: implement stream.at_end() 
        while not at_end :
            line = stream.read()
            print line,
            if line == "":
                at_end = True
                
            
                
            
    
    