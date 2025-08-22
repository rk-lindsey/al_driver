# For a seamless run on LLNL-LC (Quartz)
        
################################
##### General options
################################

#EMAIL_ADD     = "lindsey11@llnl.gov" 

ATOM_TYPES = ['C', 'N']
NO_CASES = 1

DRIVER_DIR     = "/work2/09982/aoladipupo/stampede3/codes/al_driver-LLfork/"
WORKING_DIR    = "/work2/09982/aoladipupo/stampede3/codes/al_driver-LLfork/examples/hierarch_fit/"
CHIMES_SRCDIR  = "/work2/09982/aoladipupo/stampede3/codes/chimes_lsq-LLfork/src/"

################################
##### General HPC options
################################

HPC_ACCOUNT = "TG-CHM240010"
HPC_PYTHON  = "/scratch/projects/compilers/intel24.0/oneapi/intelpython/python3.9/bin/python"
HPC_SYSTEM  = "TACC"
HPC_PPN     = 48 #for spr it has 112, for skx its 48

HPC_EMAIL     = False 

N_HYPER_SET = 1
################################
##### ChIMES LSQ
################################

ALC0_FILES    = WORKING_DIR + "ALL_BASE_FILES/ALC-0_BASEFILES/"
CHIMES_LSQ    = CHIMES_SRCDIR + "../build/chimes_lsq"
CHIMES_SOLVER = CHIMES_SRCDIR + "../build/chimes_lsq.py"
CHIMES_POSTPRC= CHIMES_SRCDIR + "../build/post_proc_chimes_lsq.py"

# Generic weight settings

WEIGHTS_FORCE = [ ["A","B"], [[1.0  ],[1.0,-1.0]] ] 
WEIGHTS_FGAS  = [ ["A","B"], [[1.0  ],[1.0,-1.0]] ] 
WEIGHTS_ENER  = [ ["A","B"], [[0.3  ],[1.0,-1.0]] ] 
WEIGHTS_EGAS  = [ ["A","B"], [[1.0  ],[1.0,-1.0]] ] 
WEIGHTS_STRES = [ ["A","B"], [[100.0],[1.0,-1.0]] ] 

REGRESS_ALG   = "dlasso"
REGRESS_VAR   = "1.0E-5"
REGRESS_NRM = True

# Stress tensor settings

#USE_AL_STRS   = 0     # A cycle number. 
STRS_STYLE    = "ALL" # Options: "DIAG" or "ALL"

CHIMES_BUILD_NODES = 1
CHIMES_BUILD_QUEUE = "skx"
CHIMES_BUILD_TIME  = "01:00:00"

CHIMES_SOLVE_NODES = 4
CHIMES_SOLVE_QUEUE = "skx" 
CHIMES_SOLVE_TIME  = "01:00:00"

################################
##### Molecular Dynamics
################################

MD_STYLE = "CHIMES"
CHIMES_MD_MPI = CHIMES_SRCDIR + "../build/chimes_md"
CHIMES_MD_SER = CHIMES_SRCDIR + "../build/chimes_md-serial"

MOLANAL  = CHIMES_SRCDIR + "../contrib/molanal/src/"
MOLANAL_SPECIES = ["C1","N"]

MD_NODES = [1] * NO_CASES
MD_QUEUE = ['skx'] * NO_CASES
MD_TIME  = ['1:00:00'] * NO_CASES

################################
##### Hierarchical fitting block
################################

DO_HIERARCH = True
HIERARCH_PARAM_FILES = ['C.params.txt.reduced', 'N.params.txt.reduced']
HIERARCH_EXE = CHIMES_MD_SER

################################
##### QM-Specific variables (Single point calculations)
################################

QM_FILES = WORKING_DIR + "ALL_BASE_FILES/QM_BASEFILES"

VASP_EXE = "/work2/09982/aoladipupo/stampede3/software/stampede_installation_scripts/vasp/vasp.5.4.4.pl2/build/gam/vasp"
VASP_TIME    = "01:00:00"
VASP_NODES = 1
VASP_PPN = 48
VASP_QUEUE = "skx"
VASP_MODULES = "mkl intel/24.0  impi/21.11" 

