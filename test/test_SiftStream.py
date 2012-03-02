#!/usr/bin/env python
import unittest
import siftstream
import siftproperty

# Not much to test on this but it shows a complete example of how to use the
# interface.

# A mock database is chosen as this may be the hardesst thing to get ones 
# head around because they are not normally used like streams or considered to be
# streams for that matter. But one can definitally implement them like a stream.

# Some databases like MS SQL have blocking data queues (Ref: Broker Server) which
# return data when an inserted row triggers the unlock. This performs exactly like 
# a blocking tcp socket read. seek is not revelant 

class DBResource(object):
    def __init__(self, username, password, servername):
        self._username = username
        self._password = password
        self._servername = servername
    
    @property 
    def username(self):
        return self._username
    
    @property
    def password(self):
        return self._password
        
    @property
    def servername(self):
        return self._servername 

class MyMockDatabaseStream(siftstream.SiftStream):
    
    def __init__(self):
        self.handle = None
        self.results = None
        
    def open(self, resource ):
        if not isinstance(resource, DBResource):
            raise Exception("resource mismatch")
        if (resource.username == "validname" and \
            resource.password == "validpass" and \
            resource.servername == "validserver" ) :
            raise Exception("Creds are not valid ones.")
        self.handle = True
        
    def close(self):
        pass
        
    def read(self, params ):
        self.handle.prepare() 
        pass
    
    def write(self, data):
        pass
        
    def prepare(query):
        """illistritive prepare"""
        if query.startswith("select"):
            self.results = [["result 1"] ,["result 2"] , ["result 3"], ["result 4"]]
        else:
            raise Exception("ONLY SELECTS PLEASE !")
            
    def seek(self):
        pass

# class MyFileStream(siftstream.SiftStream):
    # pass


class TestSiftStream(unittest.TestCase):
    
    def setUp(self):
        self.sift_stream = MyMockDatabaseStream()
        
    def test0_construct(self):
        self.assertEqual( MyMockDatabaseStream().version() , siftproperty.version() )
        
        test_obj = self.sift_stream
        self.assertTrue(test_obj)
        

        
        
         

if __name__ == "__main__":
    unittest.main()