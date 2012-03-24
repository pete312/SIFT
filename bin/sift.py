#!/usr/bin/env python
import sys
import os
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
    import logstream
    
    engines = []
    
    targetfile = normpath(join(PACKAGEPATH, 'test/samplelog1.txt'))
    #targetfile = join(basepath, 'test/samplelog1.txt')
    print targetfile
    
    if not os.path.exists(targetfile):
        sys.exit(2)
    else:
        print "It exists"
        
    log = logparser.LOGTest()
    log.prepare()
    
    stream = logstream.LogStream()
    stream.open(targetfile)
    
    
    engines.append(log)
    
    
    for e in engines:
        e.parse(stream)
    
    print log.expressions



if __name__ == "__main__":
    init()
    main()
    
    