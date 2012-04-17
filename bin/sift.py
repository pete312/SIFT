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
    



def demo1():
    import liblogparser
    import siftstream
    import siftengine
    
    
        
    targetfile = normpath(join(PACKAGEPATH, 'test/samplelog1.txt'))
    #targetfile = join(basepath, 'test/samplelog1.txt')
    print targetfile
    
    if not os.path.exists(targetfile):
        print "No input file", targetfile
        sys.exit(2)
        
    # this is a garbage collector and might rename it to be called that.
    null = siftengine.Null()
    
    # create the custom log parser object
    log = liblogparser.LOGTest()
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
    while not stream.at_end():
        for e in engines:
            e.parse(stream)
            #e.debug()

    print " the engine has a state of", log.get_state()
    print "\n... End of DEMO 1 ...\n\n"

def demo2():
    import libmultiparser
    import siftstream
    import siftengine
    
    
    targetfile = normpath(join(PACKAGEPATH, 'test/samplelog2_bad_case_for_some.txt'))
    #targetfile = join(basepath, 'test/samplelog1.txt')
    print targetfile
    
    if not os.path.exists(targetfile):
        print "No input file", targetfile
        sys.exit(2)
        
    # this is a garbage collector and might rename it to be called that.
    null = siftengine.Null()
    
    # create the custom log parser objects for each worker pattern.
    
    # this parser is looking for worker messages in the form 
    # ..6: Autonomus message <number string>
    worker_thread = libmultiparser.WorkerPattern()
    worker_thread.prepare()

    
    # The next 2 parsers are looking for 2 thread messages sequences and 
    # can initalize independantly. They both share the same codebase. all that is
    # different is the pattern that they are using to match the messages.
    # Also the worker thread is passed so that its state can be controlled.
    prime_thread = libmultiparser.ThreadInitSequence(thread=1, worker=worker_thread)
    prime_thread.prepare()
    
    aux_thread = libmultiparser.ThreadInitSequence(thread=2, worker=worker_thread)
    aux_thread.prepare()
    
    # setup the stream which points to a text file in the test path
    stream = siftstream.FileStream()
    stream.open(targetfile)
    
    # make the collection of engines. 
    # The null engine is important and should always be at the bottom to collect the garbage.
    engines = []
    engines.append(prime_thread)
    engines.append(aux_thread)
    engines.append(worker_thread)
    engines.append(null)
    
    
    # a simple while have data parse it with each engine. How simple is that!
    while not stream.at_end():
        for e in engines:
            e.parse(stream)
            #e.debug()

    for engine in engines:
        print "---", engine.name
        if type(engine) != siftengine.Null:
        
            print " engine %s has a state of %s" % ( engine.name , engine.get_state() )
            
    print "\n... End of DEMO 2 ...\n\n"
    
def main():


    print ".... DEMO 1 .... \n Use of rather simple parse defined in liblogparser.py\n"
    raw_input("Press key to start demo 1 ")
    demo1()
    
    print ".... DEMO 2 shows how to create a more complex parser defined in libmultiparse.py"
    raw_input("Press key to start demo 2 ")
    demo2()
    


if __name__ == "__main__":
    init()
    main()
    
    