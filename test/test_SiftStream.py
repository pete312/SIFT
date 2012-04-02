#!/usr/bin/env python
import unittest
import sys
import os
from os.path import dirname, normpath, join, abspath

BASEDIR = dirname(abspath(sys.argv[0]))
LIBPATH = normpath(join(BASEDIR, "../lib"))
BINPATH = normpath(join(BASEDIR, "../bin"))
sys.path.append(LIBPATH)
sys.path.append(BINPATH)

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
                    
        statement = self.prepare( self.get_sql + str( self.sequence_id ) )
        self.execute(statement)
        self.seek(0,2)
        
        self._at_end = True
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
        self._at_end = False
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
        
    @property
    def at_end(self):
        return self._at_end
        


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
        
    def test3_test_sift_filestream(self):
        """test provided File stream """
        TEMPFILE = normpath (join(BASEDIR, "file_stream.txt"))
        
        
    
    
    def test3_append_to_resource_after_read_hits_the_bottom(self):
        '''need to test that the stream can detect when data is added to the stream'''
        TEMPFILE = normpath (join(BASEDIR, "append_test.txt"))
        ofile = open(TEMPFILE, "w")
        ofile.write("line 1\n")        
        ofile.write("line 2\n")
        ofile.close()
        
        reader =  siftstream.FileStream()
        reader.open(TEMPFILE)
        
        self.assertEqual(0, reader.tell())
        
        self.assertEqual(reader.read(), "line 1\n")
        self.assertEqual(7, reader.tell()) # platform specific
        self.assertFalse(reader.at_end())
        
        self.assertEqual(reader.read(), "line 2\n")
        self.assertEqual(14, reader.tell()) # platform specific
        self.assertTrue(reader.at_end())
        
        ofile = open(TEMPFILE, "a")
        ofile.write("line 3\n")
        ofile.close()
        
        self.assertEqual(reader.read(2), "li")
        self.assertFalse(reader.at_end())
        
        self.assertEqual(reader.read(), "ne 3\n")
        self.assertTrue(reader.at_end())
        
        self.assertEqual(reader.read(), "")
        self.assertTrue(reader.at_end())
        
        ofile = open(TEMPFILE, "a")
        ofile.write("line 4\n")
        ofile.close()
        
        self.assertFalse(reader.at_end())
        self.assertEqual(reader.read(), "line 4\n")
        self.assertTrue(reader.at_end())
        
        self.assertEqual(reader.read(), "")
        self.assertTrue(reader.at_end())
        
        
        writer = siftstream.FileStream()
        writer.open(TEMPFILE, "a")
        writer.write("line 5\n")
        writer.close()
        
        self.assertEqual(reader.read() , "line 5\n")
        
        os.unlink(TEMPFILE)
        
        
    def test_tailing_works_on_platform(self):
        '''test tailing a file just in case it does not work the same on all platforms''' 
        TEMPFILE = normpath (join(BASEDIR, "append_test.txt"))
        ofile = open(TEMPFILE, "w")
        ofile.write("line 1\n")
        ofile.close()
        
        ifile = open(TEMPFILE, "r")
        buf = ifile.read()

        self.assertEqual(buf, "line 1\n")
        last_pos = ifile.tell()
        
        ifile.seek(0,2) # move to end 
        eof = ifile.tell()
        
        self.assertEqual( last_pos , eof ) 
        
        # now append 
        ofile = open(TEMPFILE, "a")
        ofile.write("line 2\n")
        ofile.close()
        
        ifile.seek(0,2)
        new_pos = ifile.tell()
        
        self.assertNotEqual(last_pos,new_pos)
        os.unlink(TEMPFILE)
        

if __name__ == "__main__":
    unittest.main()