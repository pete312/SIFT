#!/usr/bin/env python
import sys
import os

import siftengine


def test():
    print "OK"
   

class Null():
    def __init__(self):
        self.trash = None
       
    @property
    def name(self):
        return self.__class__   
    
    def parse(self,stream):
        self.trash = stream.read()
        
    def debug(self):
        print self.__class__, "contains", self.trash
                
                
            
                
            
    
    