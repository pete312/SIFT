# 
import siftstream

class LogStream(siftstream.SiftStream): 
    def __init__(self):
        self.resource = None
    
    def open(self, file):
        print "open file", file
        if self.resource == None:
            self.resource = open(file, "r")
            assert(self.resource != None)
            
            
    def close(self):
        if self.resource != None:
            self.resource.close()
            
    def read(self):
        return self.resource.readline()
    
    def write(self):
        pass
        
    def seek(self,pos,wence):
        self.resource.seek(pos, wence)
        
    def tell(self):
        return self.resource.tell()