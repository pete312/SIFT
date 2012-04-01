#!/usr/bin/env python
  
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
                