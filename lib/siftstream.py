import abc
import siftproperty

""" This class provides standard functions for basic in out operations.
 This is required for other polimorphic (generic) stream operations.
 The object may be a file, a database, a socket a middleware system 
 or other resource. """

class SiftStream( object ):

    __metaclass__ = abc.ABCMeta
    

    @staticmethod
    def version():
        return siftproperty.version()    
        
    @abc.abstractmethod
    def open(self, resource ):
        """implement open resource"""
        pass
    
    @abc.abstractmethod   
    def close(self):
        """implement close resource"""
        pass
        
    @abc.abstractmethod
    def read(self, params ):
        """implement read from resource"""
        pass
    
    @abc.abstractmethod    
    def write(self, data):
        """implement write to resource"""
        pass
        
    @abc.abstractmethod    
    def seek(self, position, whence):
        """this may not be needed by some resources such as databases in which case you can implement with the no op function (pass)"""
        pass
        
    @abc.abstractmethod    
    def tell(self):
        """implement tell"""
        pass    
