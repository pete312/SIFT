import abc
import siftproperty
import re
import sys

class SiftEngine(object):

    __metaclass__ = abc.ABCMeta
    
    def __init__(self):
        self._expressions = []
        self._compiled = []
        self._initialized = True
        self._matched = False
        self._found = 0
    
    @property
    def expressions(self):
        return self._expressions
        
    @property
    def matched(self):
        return self._matched
    
    @staticmethod
    def version():
        return siftproperty.version()

    @abc.abstractmethod
    def prepare(self):
        pass
        
    @abc.abstractmethod
    def reset(self):
        pass
        
    @abc.abstractmethod
    def on_match(self):
        """Called when the segment is finished matching"""
        pass
    
    @abc.abstractmethod
    def on_triggered(self):
        """Called when a regex matches"""
        pass
        
    def add_regex(self, regex):
    
        try: 
            self._initialized
        except AttributeError:
            print "The base class of", self , "has not been initialized. Try adding SiftEngine.__init__(self) to te ", self.__class__ , "class\n" 
            sys.exit()
            
        self._expressions.append(regex)
        obj = False
        try:
            obj = re.compile(regex)
        except Exception as e:
            print "Caught an expression error with message:",  e
            print "\tregex sequecne # :" , len(self._expressions) 
            print "\tregex string : |" + regex + "|"
            print
            raise e
        self._compiled.append(obj)
        return obj
        
    def parse(self,stream):
            
        while (not stream.at_end()) and (not self._matched):
            line = stream.read()
            pattern = self._compiled[self._found].match(line)
            if pattern:
                self._found += 1
                self.on_triggered(pattern)
                
                if self._found == len(self._compiled):
                    self._matched = True
                    self.on_match()
                
            else:
                stream.unread() # back up the pointer to pos before read()
                return
        
    
    def get_segment(self, line_number=None):
        """return the line """
        return self._expressions
        
    def debug(self):
        print self.__class__
   
   
class Null(object):
    def __init__(self):
        self.trash = None
       
    @property
    def name(self):
        return self.__class__   
    
    def parse(self,stream):
        self.trash = stream.read()
        
    def debug(self):
        print self.__class__, "contains", self.trash
        