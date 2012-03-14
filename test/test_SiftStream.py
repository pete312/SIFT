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
# a blocking tcp socket read. seek and tell are not revelant but can be implemented if the dataset has a sequence id or other watermark as shown in the mock.


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
    
    @property
    def FROM_END():
        return 2
    
    @property
    def FROM_CURRENT():
        return 1
    
    @property
    def FROM_ABSOLUTE():
        return 0
    
    def __init__(self):
        self.close()

        self.sequence_id = 0
        self.get_sql = "select stuff from data where sequence_id > "
    
    def __iter__(self):
        return self
    
    def next(self):
        raise StopIteration()
        
    def open(self, resource ):
        if not isinstance(resource, DBResource):
            raise Exception("resource mismatch")
        if (resource.username != "validname" and \
            resource.password != "validpass" and \
            resource.servername != "validserver" ) :
            raise Exception("Credentials are not valid ones.")
        self.handle = True
        
    def close(self):
        self.handle = None
        self.results = []
        self.data = []
        self.cursor = 0
        
    def read(self, size=-1 ):
        # size is implemented to return the number of rows and not number of bites
        
        #if len(self.data) == self.cursor and self.cursor > 0:
            
        statement = self.prepare( self.get_sql + str( self.sequence_id ) )
        self.execute(statement)
        self.seek(0,2)
        
        #if size < 0:
        
        return self.data
           
    def write(self, data):
        pass
        
    def prepare(self, query):
        """illistritive prepare"""
        self.results = None
        if self.handle == None:
            raise Exception("mock database not open")
        if query.startswith("select") :
            self.results = [[1,"row 1"] ,[2,"row 2"] , [3,"row 3"], [4,"row 4"]]
        else:
            raise Exception("ONLY SELECTS PLEASE ! query = [" + query + "]")
            
        return [1, "successful statement" ]
            
    def execute(self, statement):
        if statement != [1, "successful statement"]:
            raise Exception("malformed statement")
        self.data = self.results
        self.sequence_id = 1
        return self.data
            
    def seek(self, position, whence=0):
        
        if whence == 0:
            assert (postion > 0)
            if self.sequence_id - position < 0:
                raise Exception("relative seek error")
            self.sequence_id = self.sequence_id - position
        elif whence > 0:
            self.sequence_id = self.sequence_id + position
        else:
            self.sequence_id = position
       
        statement = self.prepare( self.get_sql + str(self.sequence_id) )
        self.execute(statement)
        
    def tell(self):
        return self.sequence_id
        


class TestSiftStream(unittest.TestCase):
    
    def setUp(self):
        self.sift_stream = MyMockDatabaseStream()
        
    def test0_construct(self):
        self.assertEqual( MyMockDatabaseStream().version() , siftproperty.version() )
        
        test_obj = self.sift_stream
        self.assertTrue(test_obj)

    def test1_mock_db_class_works(self):
        test_obj = self.sift_stream
        resource = DBResource("testuser","testpass","testserver")
        self.assertRaises(Exception, test_obj.open, resource)    
        resource = DBResource("valieduser","validpass","validserver")
        self.assertRaises(Exception, test_obj.open, None)
        
        test_obj.open(resource)
        self.assertRaises(Exception, test_obj.prepare, "insert into whatever")
     
        self.assertRaises(Exception, test_obj.execute, None)
        
        #test a good case.
        statement = test_obj.prepare("select whatever")
        results = test_obj.execute(statement)
        
        self.assertTrue( len(results) > 0 )
        
        for row in results:
            self.assertEqual(len(row) ,  2 )
            
        self.assertTrue( test_obj.tell()  > 0 )
    
        
    def test2_getting_something_out_of_it(self):
        test_obj = self.sift_stream
        self.assertEqual(test_obj.tell(), 0)
        test_obj.open(DBResource("validuser", "validpass", "validserver"))
        test_obj.seek(0,MyMockDatabaseStream.FROM_END)
        
        row_number = 0
        for row in test_obj.read():
            row_number += 1
            self.assertEqual(row_number, row[0]) 
            
        test_obj.close()
        
       
        
        
        

if __name__ == "__main__":
    unittest.main()