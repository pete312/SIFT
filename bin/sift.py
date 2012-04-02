#!/usr/bin/env python
import sys
import os
import time
from os.path import dirname, normpath, join, abspath

PACKAGEPATH = ''
LIBPATH = ''
BINPATH = ''

def options(argv):
    runoptions = {} 
    return runoptions 

def init():
    # work out the paths and add them to the python path
    global LIBPATH 
    global PACKAGEPATH
    global BINPATH
    PACKAGEPATH = normpath(join(abspath(dirname(sys.argv[0])), "..")) 
    LIBPATH = normpath(join(PACKAGEPATH, "lib"))
    BINPATH = normpath(join(PACKAGEPATH, "bin"))
    sys.path.append(LIBPATH)
    sys.path.append(BINPATH)
    


def main():

    import logparser
    import null
    import siftstream
    
    
    targetfile = normpath(join(PACKAGEPATH, 'test/samplelog1.txt'))
    #targetfile = join(basepath, 'test/samplelog1.txt')
    print targetfile
    
    if not os.path.exists(targetfile):
        print "No input file", targetfile
        sys.exit(2)
        
    # this is a garbage collector and might rename it to be called that.
    null = null.Null()
    
    # create the custom log parser object
    log = logparser.LOGTest()
    log.prepare()
    
    # display what this engine will be looking for in the stream.
    print "looking for paragraph"
    for expression in log.expressions:
        print expression
    print 
    
    # setup the stream which points to a text file in the test path
    stream = siftstream.FileStream()
    stream.open(targetfile)
    
    # make the collection of engines. 
    # The null engine is important and should always be at the bottom to collect the garbage.
    engines = []
    engines.append(log)
    engines.append(null)
    
    # a simple while have data parse it with each engine. How simple is that!
    while not stream.at_end:
        for e in engines:
            e.parse(stream)
            #e.debug()
    
    



if __name__ == "__main__":
    init()
    main()
    
    