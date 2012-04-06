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

    @abc.abstractproperty
    def at_end(self):
        """implement this property to return true if there is no more data in stream"""
        pass
        
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
        
        
class FileStream(SiftStream): 
    def __init__(self):
        self.resource = None
        self._at_end = False
        self._unread = False
        self._tell = 0
        self._tail = 0
    
    def open(self, file, mode="r"):
        self.resource = open(file, mode)
              
    def close(self):
        if self.resource != None:
            self.resource.close()
                
    def read(self, size=None):
        
        if self._unread:
            self._unread = False
            return self._safe
        else:
            if size:
                self._safe = self.resource.read(size)
            else:
                self._safe = self.resource.readline()
            self._tell = self.tell()
            if self._safe == "":
                self._tail = self._tell
        return self._safe
    
    def write(self, data):
        if self.resource != None:
            return self.resource.write(data)
        
    def at_end(self):
        
        self._tell = self.tell()  # make sure we have currnet pos
        self.seek(0,2)
        self._tail = self.tell()
        self.seek(self._tell, 0)
        
        if self._tail == self._tell:
            return True
        else:    
            return False
            
        
    def unread(self):
        self._unread = True
        
    def seek(self,pos,wence):
        self.resource.seek(pos, wence)
        
    def tell(self):
        return self.resource.tell()
        
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
        
# TODO: provide SocketStream

