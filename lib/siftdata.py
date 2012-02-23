import siftproperty

class SiftData(object):
    def __init__(self):
        pass
        
        
    dic_data = property(store, peek, pop)
    
    @classmethod 
    def version():
        return siftproperty.version()
    
    def pull(self):
        return self._data
        
    def push(self, data):
        self._dic_data = data
        
    def ddelete(self):
        self._dic_data.clear()
        
    
    def 