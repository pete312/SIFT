import siftproperty

class SiftData(object):
    def __init__(self):
        
        self.list_data = []
        self.dic_data = {}
    
    @classmethod 
    def version():
        return siftproperty.version()
    
    def pop_back(self):
        """pop off the back of the list"""
        return self.list_data.pop()
        
    def push_back(self, data):
        """push to the back of the list"""
        self.list_data.append(data)
        
    def pop_front(self):
        """pop off the front of the list"""
        return self.list_data.pop()
        
    def push_front(self, data):
        """push to the front of the list"""
        self.list_data.append(data)
        
    def store(self, key, data):
        """unordered save"""
        self.dic_data[key] = data
        
    def peek(self, key):
         """get value if exists"""
        return False
        
    def has(self, key):
        return self.dic_data.has_key()

    def delete(self):
        self._dic_data.clear()
        
    
    