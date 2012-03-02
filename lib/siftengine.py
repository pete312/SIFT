import abc
import siftproperty

class SiftEngine(object):

    __metaclass__ = abc.ABCMeta
    
    @abc.abstractproperty
    def expressions(self):
        pass
    
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
        self._expressions.append(regex)
        pass
    
    def get_segment(self, line_number=None):
        """return the line """
        return self._expressions
    
    def get_state(self):
        #TODO define in siftstate
        pass
        
   
    
        