import siftproperty

class Empty(Exception):
    pass
    
class SiftData(object):
    def __init__(self):
        
        self.list_data = []
        self.dic_data = {}
    
    @staticmethod 
    def version():
        return siftproperty.version()
        
        
    def _thow_on_empty(self, associative=False):
        if associative:
            if len(self.dic_data) == 0:
                raise Empty("No data")
        else:
            if len(self.list_data) == 0:
                raise Empty("No data")
    
    def pop_back(self):
        """pop off the back of the list"""
        self._thow_on_empty()
        return self.list_data.pop()

        
    def push_back(self, data):
        """push to the back of the list"""
        self.list_data.append(data)
        
    def pop_front(self):
        """pop off the front of the list"""
        self._thow_on_empty()
        return self.list_data.pop(0)
        
    def push_front(self, data):
        """push to the front of the list"""
        self.list_data.append(data)
        
    def store(self, key, data):
        """unordered save"""
        self.dic_data[key] = data
        
    def peek(self, key):
        """get value if exists"""
        self._thow_on_empty(True)
        return self.dic_data[key]
        
    def has(self, key):
        return self.dic_data.has_key(key)

    def delete(self):
        self.dic_data.clear()
        self.list_data = []
        
    
    