#!/usr/bin/env python
import unittest
import sys
import os
from os.path import dirname, normpath, join, abspath

basedir = dirname(abspath(sys.argv[0]))
libpath = normpath(join(basedir, "../lib"))
sys.path.append(libpath)

import siftengine
import siftproperty
import siftstate
import siftdata
import siftstream
import collections
import logging
import time


class CachingStream(siftstream.SiftStream,siftdata.SiftData):
    def __init__(self):
        self._buffer = ""
        self._cache = collections.deque()
        self.resource = None
        self._is_open = False
        self._at_end = False
     
    def get_cache(self):
        return self._cache
        
    def load_cache(self):
        self._cache.append(self.readlines())
        
    def clear_cache(self):
        self._cache = None
        
    cache = property(get_cache, load_cache, clear_cache)
    
    @property
    def is_open(self):
        return self._is_open
    
    def open(self, resource):
        self.resource = open(resource)
        self._is_open = True
        return self.resource
        
    def close(self):
        if self.resource:
            self.resource.close()
            self.resource = None
            self._is_open = False
    
    def seek(self, position, whence):
        """its going to throw if its not opened first"""
        return self.resource.seek(position,whence)
        
    def tell(self):
        """its going to throw if its not opened first"""
        return self.resource.tell()
        
    def read_line(self):
        assert(self.is_open)
        return self.resource.read(size)
        
    def readlines(self):
        assert(self.is_open)
        self._at_end = True
        return self.resource.readlines()
        
    def read(self, size=-1):
        assert(self.is_open)
        return self.resource.read(size)
        
    def write(self, buffer):
        assert(self.is_open)
        self.resource.write(buffer)
    
    @property
    def at_end(self):
        return self._at_end
        

class TestEngine(siftengine.SiftEngine, siftstate.SiftState):
    def __init__(self, triggered_callback, match_callback):
        siftengine.SiftEngine.__init__(self)
        siftstate.SiftState.__init__(self)
        self._triggered_callback = triggered_callback
        self._match_callback = match_callback
    
        self._expressions = ['dummy']
        self._matched_count = 0
        self._trigger_count = 0
    
    @property
    def matched_count(self):
        return self._matched_count
        
    @property
    def trigger_count(self):
        return self._trigger_count
    
    def prepare(self):
        self.add_regex("regex one")
        self.add_regex("regex two")
        self.reset()

    def reset(self):
        self._found = 0
        self._matched = False
        
    def on_match(self):
        self._match_callback()
        
    def on_triggered(self, pattern):
        print "here"
        self._triggered_callback(pattern)
    
    def on_change(self):
        pass
        
        
class Visitor(siftengine.SiftEngine):
    def __init__(self, pattern ):
        siftengine.SiftEngine.__init__(self)
        self.visits = 0
        
        self.add_regex(pattern)
        
    def prepare(self):
        self.reset()
        
    def reset(self):
        pass
        
    def on_match(self):
        pass
        
    def on_triggered(self):
        pass
        
    

         
     
class TestSiftEngine(unittest.TestCase):
    
    def setUp(self):
        self.sift_engine = TestEngine(self.triggered_callback, self.matched_callback);
        
        
    def tearDown(self):
    
        #cleanup any files this test produces.
        try:
            #pass
            os.remove("local.log")
        except OSError:
            # its ok if the file is not there
            pass
            
    def matched_callback(self):
        print "matched im in here"
            
    def triggered_callback(self, pattern):
        print "im here", pattern.groups() 
    
    def test0_construct(self):
        self.assertTrue( self.sift_engine )
        self.assertEqual( siftproperty.version(), self.sift_engine.version() )
        
    def test1_add_expression(self):
        test_obj = self.sift_engine
        test_obj.prepare()
        empty = TestEngine(self.triggered_callback, self.matched_callback)
        self.assertEqual(['dummy','regex one', 'regex two'], test_obj.get_segment() )
        self.assertEqual( ['dummy'], empty.get_segment() )
        
        

    def test2_test_engine(self):
        test_obj = self.sift_engine
        resource = CachingStream()
        
        START = "It's a start"
        END = "That's a wrap"
        CR = "\n" # WARNING this may change from system to system.
        
        LOG_FORMAT = '%(message)s'
        logging.basicConfig(filename="local.log", level=logging.DEBUG, format=LOG_FORMAT)
        self.assertTrue( resource.open("local.log") )        
        
        logging.info(START)
        self.assertEqual([START + CR ] , resource.readlines() )
                
        logging.info(END)
        self.assertEqual([END + CR ] , resource.readlines() )
        
        resource.seek(0,0)
        self.assertEqual([START + CR, END + CR ] , resource.readlines() )
                
        #resource.load_cache()

        resource.close()
        logging.shutdown()
        
        
    def test3_test_parse_trigger_and_matched(self):
    
        class NewTest(TestEngine):
            def __init__(self, trigger_callback, match_callback):
                TestEngine.__init__(self, trigger_callback, match_callback)
                
            def prepare(self):
                self.add_regex("regex one (d+)")
                self.add_regex("regex two (d+)")
            
            
                
        test_obj = NewTest(self.triggered_callback, self.matched_callback)
        LOG_FORMAT = '%(message)s'
        logging.basicConfig(filename="local.log", level=logging.DEBUG, format=LOG_FORMAT)
        logging.info("this\n")

        f = open("local.log")
        print f.readlines()
        f.close()
        stream = siftstream.FileStream()
        #self.assertTrue( stream.open("local.log") )
        self.assertTrue( os.path.exists("local.log") )
        self.assertTrue( stream.open("./local.log")  )
        
        logging.info("this is the last line")
        logging.shutdown()
        
    
    # make sure each engine is visited before a line is collected as garbage.
    def test_visitation(self):
        c  = siftengine.Collector() 
        c.add_engine(Visitor("one"))
        c.add_engine(Visitor("two"))
        
        LOG_FORMAT = '%(message)s'
        logging.basicConfig(filename="local.log", level=logging.DEBUG, format=LOG_FORMAT)
        
        logging.warn("no match for me")
        
        f = open("./local.log")
        print f.readlines()
      
        
        #self.assertTrue( os.path.exists("lofcal.log") )
        stream = siftstream.FileStream()
        self.assertTrue(  stream.open("./local.log") )
        
        c.parse(stream)
        
    
    
if __name__ == "__main__":
	unittest.main()
    
    
    