#!/usr/bin/env python3
"""
Run regresion tests on a parameterized bitcell
"""

import unittest
from testutils import header,openram_test
import sys,os
sys.path.append(os.path.join(sys.path[0],".."))
import globals
from globals import OPTS
import debug

OPTS = globals.OPTS

#@unittest.skip("SKIPPING 04_pbitcell_test")
class pbitcell_test(openram_test):

    def runTest(self):
        globals.init_openram("config_20_{0}".format(OPTS.tech_name))
        from pbitcell import pbitcell
        import tech
        OPTS.num_rw_ports=1
        OPTS.num_w_ports=1
        OPTS.num_r_ports=1
        debug.info(2, "Bitcell with 1 of each port: read/write, write, and read")
        tx = pbitcell()
        self.local_check(tx)
        
        OPTS.num_rw_ports=0
        OPTS.num_w_ports=1
        OPTS.num_r_ports=1
        debug.info(2, "Bitcell with 0 read/write ports")
        tx = pbitcell()
        self.local_check(tx)
        
        OPTS.num_rw_ports=1
        OPTS.num_w_ports=0
        OPTS.num_r_ports=1
        debug.info(2, "Bitcell with 0 write ports")
        tx = pbitcell()
        self.local_check(tx)
        
        OPTS.num_rw_ports=1
        OPTS.num_w_ports=1
        OPTS.num_r_ports=0
        debug.info(2, "Bitcell with 0 read ports")
        tx = pbitcell()
        self.local_check(tx)
        
        OPTS.num_rw_ports=1
        OPTS.num_w_ports=0
        OPTS.num_r_ports=0
        debug.info(2, "Bitcell with 0 read ports and 0 write ports")
        tx = pbitcell()
        self.local_check(tx)

        OPTS.num_rw_ports=2
        OPTS.num_w_ports=2
        OPTS.num_r_ports=2
        debug.info(2, "Bitcell with 2 of each port: read/write, write, and read")
        tx = pbitcell()
        self.local_check(tx)
        
        OPTS.num_rw_ports=0
        OPTS.num_w_ports=2
        OPTS.num_r_ports=2
        debug.info(2, "Bitcell with 0 read/write ports")
        tx = pbitcell()
        self.local_check(tx)
        
        OPTS.num_rw_ports=2
        OPTS.num_w_ports=0
        OPTS.num_r_ports=2
        debug.info(2, "Bitcell with 0 write ports")
        tx = pbitcell()
        self.local_check(tx)
        
        OPTS.num_rw_ports=2
        OPTS.num_w_ports=2
        OPTS.num_r_ports=0
        debug.info(2, "Bitcell with 0 read ports")
        tx = pbitcell()
        self.local_check(tx)
        
        OPTS.num_rw_ports=2
        OPTS.num_w_ports=0
        OPTS.num_r_ports=0
        debug.info(2, "Bitcell with 0 read ports and 0 write ports")
        tx = pbitcell()
        self.local_check(tx)

        globals.end_openram()



# instantiate a copy of the class to actually run the test
if __name__ == "__main__":
    (OPTS, args) = globals.parse_args()
    del sys.argv[1:]
    header(__file__, OPTS.tech_name)
    unittest.main()
