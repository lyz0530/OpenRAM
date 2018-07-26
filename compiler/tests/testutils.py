import unittest,warnings
import sys,os,glob,copy
sys.path.append(os.path.join(sys.path[0],".."))
from globals import OPTS
import debug

class openram_test(unittest.TestCase):
    """ Base unit test that we have some shared classes in. """
    
    def local_drc_check(self, w):

        self.reset()

        tempgds = OPTS.openram_temp + "temp.gds"
        w.gds_write(tempgds)
        import verify

        result=verify.run_drc(w.name, tempgds)
        if result != 0:
            self.fail("DRC failed: {}".format(w.name))

        self.cleanup()
    
    def local_check(self, a, final_verification=False):

        self.reset()
        
        tempspice = OPTS.openram_temp + "temp.sp"
        tempgds = OPTS.openram_temp + "temp.gds"

        a.sp_write(tempspice)
        a.gds_write(tempgds)

        import verify
        result=verify.run_drc(a.name, tempgds)
        if result != 0:
            self.fail("DRC failed: {}".format(a.name))

            
        result=verify.run_lvs(a.name, tempgds, tempspice, final_verification)
        if result != 0:
            self.fail("LVS mismatch: {}".format(a.name))

        if OPTS.purge_temp:
            self.cleanup()

    def cleanup(self):
        """ Reset the duplicate checker and cleanup files. """
        files = glob.glob(OPTS.openram_temp + '*')
        for f in files:
            # Only remove the files
            if os.path.isfile(f):
                os.remove(f)        

    def reset(self):
        """ 
        Reset everything after each test.
        """
        # Reset the static duplicate name checker for unit tests.
        import hierarchy_design
        hierarchy_design.hierarchy_design.name_map=[]
        


    def isclose(self,key,value,actual_value,error_tolerance=1e-2):
        """ This is used to compare relative values. """
        import debug
        relative_diff = abs(value - actual_value) / max(value,actual_value)
        check = relative_diff <= error_tolerance
        if not check:
            debug.warning("NOT CLOSE\t{0: <10}\t{1:.3f}\t{2:.3f}\tdiff={3:.1f}%".format(key,value,actual_value,relative_diff*100))
            return False
        else:
            debug.info(2,"CLOSE\t{0: <10}\t{1:.3f}\t{2:.3f}\tdiff={3:.1f}%".format(key,value,actual_value,relative_diff*100))
            return True

    def relative_compare(self, value,actual_value,error_tolerance):
        """ This is used to compare relative values. """
        if (value==actual_value): # if we don't need a relative comparison!
            return True
        return (abs(value - actual_value) / max(value,actual_value) <= error_tolerance)

    def isapproxdiff(self, f1, f2, error_tolerance=0.001):
        """Compare two files.

        Arguments:
        
        f1 -- First file name
        
        f2 -- Second file name

        Return value:
        
        True if the files are the same, False otherwise.
        
        """
        import re
        import debug

        numeric_const_pattern = r"""
        [-+]? # optional sign
        (?:
        (?: \d* \. \d+ ) # .1 .12 .123 etc 9.1 etc 98.1 etc
        |
        (?: \d+ \.? ) # 1. 12. 123. etc 1 12 123 etc
        )
        # followed by optional exponent part if desired
        (?: [Ee] [+-]? \d+ ) ?
        """
        rx = re.compile(numeric_const_pattern, re.VERBOSE)
        with open(f1, 'rb') as fp1, open(f2, 'rb') as fp2:
            while True:
                b1 = fp1.readline().decode('utf-8')
                b2 = fp2.readline().decode('utf-8')
                #print "b1:",b1,
                #print "b2:",b2,

                # 1. Find all of the floats using a regex
                b1_floats=rx.findall(b1)
                b2_floats=rx.findall(b2)
                debug.info(3,"b1_floats: "+str(b1_floats))
                debug.info(3,"b2_floats: "+str(b2_floats))
        
                # 2. Remove the floats from the string
                for f in b1_floats:
                    b1=b1.replace(f,"",1)
                for f in b2_floats:
                    b2=b2.replace(f,"",1)
                #print "b1:",b1,
                #print "b2:",b2,
            
                # 3. Check if remaining string matches
                if b1 != b2:
                    self.fail("MISMATCH Line: {0}\n!=\nLine: {1}".format(b1,b2))

                # 4. Now compare that the floats match
                if len(b1_floats)!=len(b2_floats):
                    self.fail("MISMATCH Length {0} != {1}".format(len(b1_floats),len(b2_floats)))
                for (f1,f2) in zip(b1_floats,b2_floats):
                    if not self.relative_compare(float(f1),float(f2),error_tolerance):
                        self.fail("MISMATCH Float {0} != {1}".format(f1,f2))

                if not b1 and not b2:
                    return



    def isdiff(self,file1,file2):
        """ This is used to compare two files and display the diff if they are different.. """
        import debug
        import filecmp
        import difflib
        check = filecmp.cmp(file1,file2)
        if not check:
            debug.info(2,"MISMATCH {0} {1}".format(file1,file2))
            f1 = open(file1,"r")
            s1 = f1.readlines()
            f2 = open(file2,"r")
            s2 = f2.readlines()
            for line in difflib.unified_diff(s1, s2):
                debug.info(3,line)
            self.fail("MISMATCH {0} {1}".format(file1,file2))
        else:
            debug.info(2,"MATCH {0} {1}".format(file1,file2))


def header(filename, technology):
    # Skip the header for gitlab regression
    import getpass
    if getpass.getuser() == "gitlab-runner":
        return
    
    tst = "Running Test for:"
    print("\n")
    print(" ______________________________________________________________________________ ")
    print("|==============================================================================|")
    print("|=========" + tst.center(60) + "=========|")
    print("|=========" + technology.center(60) + "=========|")
    print("|=========" + filename.center(60) + "=========|")
    from  globals import OPTS
    print("|=========" + OPTS.openram_temp.center(60) + "=========|")
    print("|==============================================================================|")
