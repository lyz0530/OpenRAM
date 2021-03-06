#!/usr/bin/env python3
"""
Run regression tests on a parameterized nand 2.  This module doesn't
generate a multi_finger 2-input nand gate.  It generates only a minimum
size 2-input nand gate.
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

class pnand2_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        import pnand2
        import tech

        debug.info(2, "Checking 2-input nand gate")
        tx = pnand2.pnand2(size=1)
        self.local_check(tx)

        globals.end_openram()
        

# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
