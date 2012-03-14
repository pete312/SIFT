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


class CachingStream(siftstream.SiftStream,siftdata.SiftData):
    def __init__(self):
        self._buffer = ""
        self._cache = collections.deque()
        self.resource = None
        self._is_open = False
     
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
        return self.resource.readlines()
        
    def read(self, size=-1):
        assert(self.is_open)
        return self.resource.read(size)
        
    def write(self, buffer):
        assert(self.is_open)
        self.resource.write(buffer)
        

class TestEngine(siftengine.SiftEngine, siftstate.SiftState):
    def __init__(self):
        siftengine.SiftEngine.__init__(self)
        siftstate.SiftState.__init__(self)
    
        self._expressions = ['dummy']
        self._matched_count = 0
        self._trigger_count = 0
    
    @property
    def matched_count(self):
        return self._matched_count
        
    @property
    def trigger_count(self):
        return self._trigger_count
    
    @property
    def expressions(self):
        return self._expressions
        
    def prepare(self):
        self.add_regex("regex one")
        self.add_regex("regex two")
        return True

    def reset(self):
        return True
        
    def on_match(self):
        return True
        
    def on_triggered(self):
        return True
    
    def on_leave(self):
        pass
        
    def on_enter(self):
        pass
         
     
class TestSiftEngine(unittest.TestCase):
    
    def setUp(self):
        self.sift_engine = TestEngine();
        
        
    def tearDown(self):
    
        #cleanup any files this test produces.
        try:
            os.remove("local.log")
        except OSError:
            # its ok if the file is not there
            pass
    
    def test0_construct(self):
        self.assertTrue( self.sift_engine )
        self.assertEqual( siftproperty.version(), self.sift_engine.version() )
        
    def test1_add_expression(self):
        test_obj = self.sift_engine
        test_obj.prepare()
        empty = TestEngine()
        self.assertEqual(['dummy','regex one', 'regex two'], test_obj.get_segment() )
        self.assertEqual( ['dummy'], empty.get_segment() )
        
        
    def notest(self):
        d = collections.deque([["one"],["two"],["three"]])
       
        print d[1]
        d.append(["four"])
        print d
        

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
    
    
if __name__ == "__main__":
	unittest.main()
    