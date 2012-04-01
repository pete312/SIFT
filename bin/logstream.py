# 
import siftstream

class LogStream(siftstream.SiftStream): 
    def __init__(self):
        self.resource = None
        self._at_end = False
        self._unread = False
    
    def open(self, file):
        print "open file", file
        if self.resource == None:
            self.resource = open(file, "r")
            assert(self.resource != None)
            
            
    def close(self):
        if self.resource != None:
            self.resource.close()
            
    def read(self):
        if self._unread:
            self._unread = False
            print self._safe
            return self._safe
        else:
            self._safe = self.resource.readline()
            print self._safe
            if self._safe == "":
                self._at_end = True
        return self._safe
    
    def write(self):
        pass
        
    @property 
    def at_end(self):
        return self._at_end
        
    def unread(self):
        self._unread = True
        
        
    def seek(self,pos,wence):
        self.resource.seek(pos, wence)
        
    def tell(self):
        return self.resource.tell()