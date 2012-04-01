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
    import logstream
    
    engines = []
    
    targetfile = normpath(join(PACKAGEPATH, 'test/samplelog1.txt'))
    #targetfile = join(basepath, 'test/samplelog1.txt')
    print targetfile
    
    if not os.path.exists(targetfile):
        print "No input file", targetfile
        sys.exit(2)
        
    log = logparser.LOGTest()
    log.prepare()
    
    null = null.Null()
    
    
    
    stream = logstream.LogStream()
    stream.open(targetfile)
    
    
    engines.append(log)
    engines.append(null)
    
    while not stream.at_end:
        for e in engines:
            e.parse(stream)
            #e.debug()
    
    print log.expressions



if __name__ == "__main__":
    init()
    main()
    
    