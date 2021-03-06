import sys
import datetime
import getpass
import debug
from globals import OPTS, print_time
from sram_config import sram_config
    
class sram():
    """
    This is not a design module, but contains an SRAM design instance.
    It could later try options of number of banks and oganization to compare
    results.
    We can later add visualizer and other high-level functions as needed.
    """
    def __init__(self, sram_config, name):

        sram_config.compute_sizes()
        sram_config.set_local_config(self)
        
        # reset the static duplicate name checker for unit tests
        # in case we create more than one SRAM
        from design import design
        design.name_map=[]

        debug.info(2, "create sram of size {0} with {1} num of words {2} banks".format(self.word_size, 
                                                                                       self.num_words,
                                                                                       self.num_banks))
        start_time = datetime.datetime.now()

        self.name = name

        
        if self.num_banks == 1:
            from sram_1bank import sram_1bank as sram
        elif self.num_banks == 2:
            from sram_2bank import sram_2bank as sram
        elif self.num_banks == 4:
            from sram_4bank import sram_4bank as sram
        else:
            debug.error("Invalid number of banks.",-1)

        self.s = sram(name, sram_config)  
        self.s.create_netlist()
        if not OPTS.netlist_only:
            self.s.create_layout()
        
        if not OPTS.is_unit_test:
            print_time("SRAM creation", datetime.datetime.now(), start_time)

    
    def sp_write(self,name):
        self.s.sp_write(name)

    def gds_write(self,name):
        self.s.gds_write(name)

    def verilog_write(self,name):
        self.s.verilog_write(name)

        
    def save(self):
        """ Save all the output files while reporting time to do it as well. """

        # Save the spice file
        start_time = datetime.datetime.now()
        spname = OPTS.output_path + self.s.name + ".sp"
        print("SP: Writing to {0}".format(spname))
        self.s.sp_write(spname)
        print_time("Spice writing", datetime.datetime.now(), start_time)

        # Save the extracted spice file
        if OPTS.use_pex:
            start_time = datetime.datetime.now()
            # Output the extracted design if requested
            sp_file = OPTS.output_path + "temp_pex.sp"
            verify.run_pex(self.s.name, gdsname, spname, output=sp_file)
            print_time("Extraction", datetime.datetime.now(), start_time)
        else:
            # Use generated spice file for characterization
            sp_file = spname

        # Characterize the design
        start_time = datetime.datetime.now()
        from characterizer import lib
        print("LIB: Characterizing... ")
        if OPTS.analytical_delay:
            print("Using analytical delay models (no characterization)")
        else:
            if OPTS.spice_name!="":
                print("Performing simulation-based characterization with {}".format(OPTS.spice_name))
            if OPTS.trim_netlist:
                print("Trimming netlist to speed up characterization.")
        lib(out_dir=OPTS.output_path, sram=self.s, sp_file=sp_file)
        print_time("Characterization", datetime.datetime.now(), start_time)

        if not OPTS.netlist_only:
            # Write the layout
            start_time = datetime.datetime.now()
            gdsname = OPTS.output_path + self.s.name + ".gds"
            print("GDS: Writing to {0}".format(gdsname))
            self.s.gds_write(gdsname)
            print_time("GDS", datetime.datetime.now(), start_time)

            # Create a LEF physical model
            start_time = datetime.datetime.now()
            lefname = OPTS.output_path + self.s.name + ".lef"
            print("LEF: Writing to {0}".format(lefname))
            self.s.lef_write(lefname)
            print_time("LEF", datetime.datetime.now(), start_time)

        # Write a verilog model
        start_time = datetime.datetime.now()
        vname = OPTS.output_path + self.s.name + ".v"
        print("Verilog: Writing to {0}".format(vname))
        self.s.verilog_write(vname)
        print_time("Verilog", datetime.datetime.now(), start_time)
