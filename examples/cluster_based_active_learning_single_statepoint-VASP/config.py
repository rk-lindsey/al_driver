# For a seamless run on LLNL-LC (Ruby)
        
################################
##### General options
################################

ATOM_TYPES = ['O', 'H']
NO_CASES = 1

DRIVER_DIR     = "/p/lustre3/lindsey11/al_driver-myLLfork/"
WORKING_DIR    = "/p/lustre3/lindsey11/al_driver-myLLfork/examples/cluster_based_active_learning_single_statepoint-VASP/"
CHIMES_SRCDIR  = "/p/lustre3/lindsey11/test_chimes_lsq-for-LL_to_ext_PR/chimes_lsq-LLfork/src/"

################################
##### General HPC options
################################

HPC_ACCOUNT = "iap"
HPC_PYTHON  = "/usr/tce/bin/python3"
HPC_SYSTEM  = "slurm"
HPC_PPN     = 56 # Ruby has 56

HPC_EMAIL     = False 

################################
##### ChIMES LSQ
################################

ALC0_FILES    = WORKING_DIR + "ALL_BASE_FILES/ALC-0_BASEFILES/"
CHIMES_LSQ    = CHIMES_SRCDIR + "../build/chimes_lsq"
CHIMES_SOLVER = CHIMES_SRCDIR + "../build/chimes_lsq.py"
CHIMES_POSTPRC= CHIMES_SRCDIR + "../build/post_proc_chimes_lsq.py"

# Generic weight settings

WEIGHTS_FORCE = [ ["A"], [[1.0  ]] ] 
WEIGHTS_FGAS  = [ ["A"], [[1.0  ]] ] 
WEIGHTS_ENER  = [ ["A"], [[0.3  ]] ] 
WEIGHTS_EGAS  = [ ["A"], [[1.0  ]] ] 
WEIGHTS_STRES = [ ["A"], [[100.0]] ] 

REGRESS_ALG   = "dlasso"
REGRESS_VAR   = "1.0E-5"
REGRESS_NRM = True

# Stress tensor settings

STRS_STYLE    = "ALL" # Options: "DIAG" or "ALL"

CHIMES_BUILD_NODES = 1
CHIMES_BUILD_QUEUE = "pdebug"
CHIMES_BUILD_TIME  = "01:00:00"

CHIMES_SOLVE_NODES = 2
CHIMES_SOLVE_QUEUE = "pdebug" 
CHIMES_SOLVE_TIME  = "01:00:00"

################################
##### Do Cluster-based active learning
################################

DO_CLUSTER = True
MAX_CLUATM = 10
TIGHT_CRIT = WORKING_DIR + "ALL_BASE_FILES/tight_bond_crit.dat"
LOOSE_CRIT = WORKING_DIR + "ALL_BASE_FILES/loose_bond_crit.dat"
CLU_CODE   = "/p/lustre3/lindsey11/al_driver-myLLfork/utilities/new_ts_clu.cpp"

MEM_BINS = 40
MEM_CYCL = MEM_BINS/10
MEM_NSEL = 100
MEM_ECUT = 4000.0 #  Set ATMENER false in run_md.cluster # 500.0 # Updated from 100 since now md code includes atom energy offsets

CALC_REPO_ENER_CENT_QUEUE = "pdebug" 
CALC_REPO_ENER_CENT_TIME = "1:00:00" 

CALC_REPO_ENER_QUEUE =  "pdebug"
CALC_REPO_ENER_TIME  =  "1:00:00"


################################
##### Molecular Dynamics
################################

MD_STYLE = "CHIMES"
CHIMES_MD_MPI = CHIMES_SRCDIR + "../build/chimes_md"
CHIMES_MD_SER = CHIMES_SRCDIR + "../build/chimes_md-serial"

MOLANAL  = CHIMES_SRCDIR + "../contrib/molanal/src/"
MOLANAL_SPECIES = ["H2O","H3O", "OH"]

MD_NODES = [1] * NO_CASES
MD_QUEUE = ['pdebug'] * NO_CASES
MD_TIME  = ['00:05:00'] * NO_CASES

################################
##### QM-Specific variables (Single point calculations)
################################

QM_FILES = WORKING_DIR + "ALL_BASE_FILES/QM_BASEFILES"

VASP_EXE = "/p/lustre3/lindsey11/vasp_std.5.4.4"
VASP_TIME    = "01:00:00"
VASP_NODES = 1
VASP_PPN = 56
VASP_QUEUE = "pdebug"
VASP_MODULES = "intel-classic/19.1.2 mvapich2/2.3.6 mkl"
