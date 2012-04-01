#!/usr/bin/env python

import siftengine


class LOGTest(siftengine.SiftEngine):
    def __init__(self):
        siftengine.SiftEngine.__init__(self)
        self.leader = '\.\.(\d+)\: '
        self._found = None
        self._group = []
    
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
        self.reset()
        
    def on_triggered(self,pattern):
        '''this callback is triggered every time a line is found that is a submatch for the engine'''
        print "triggered a sub match for" , self.__class__, self._found
        self._group.append(pattern.groups())
        
        
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
    
    def parse(self,stream):
            
        while (not stream.at_end) and (not self._matched):
            line = stream.read()
            pattern = self._compiled[self._found].match(line)
            if pattern:
                self._found += 1
                self.on_triggered(pattern)
                
                print "-- " , self._found, len(self._compiled)
                
                if self._found == len(self._compiled):
                    self._matched = True
                    self.on_match()
                
            else:
                stream.unread() # back up the pointer to pos before read()
                return
                
    def debug(self):
        print self.__class__, "found", self._found
        
                
                
            
                
            
    
    