#!/usr/bin/env python
import unittest
import sys
from os.path import dirname, normpath, join, abspath
basedir = dirname(abspath(sys.argv[0]))
libpath = normpath(join(basedir, "../lib"))
binpath = normpath(join(basedir, "../bin"))
sys.path.append(libpath)
sys.path.append(binpath)

import sift

class TestSiftMain(unittest.TestCase):
    def test_main(self):
        pass



if __name__ == "__main__":    
    unittest.main()
    