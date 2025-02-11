# Configured for seamless run on LLNL-LC (Quartz)

################################
##### General options
################################

#EMAIL_ADD = "awwalola@umich.edu"

ATOM_TYPES     = ["C"]
NO_CASES       = 1
USE_AL_STRS    = -1
DRIVER_DIR     = "/work2/09982/aoladipupo/stampede3/codes/al_driver-LLfork/"
WORKING_DIR    = "/work2/09982/aoladipupo/stampede3/codes/al_driver-LLfork/examples/simple_iter_single_statepoint-lmp-test-turbo-test/"
CHIMES_SRCDIR  = "/work2/09982/aoladipupo/stampede3/codes/chimes_lsq-LLfork/src/"

################################
##### ChIMES LSQ
################################

ALC0_FILES    = WORKING_DIR + "ALL_BASE_FILES/ALC-0_BASEFILES/"
CHIMES_LSQ    = CHIMES_SRCDIR + "../build/chimes_lsq"
CHIMES_SOLVER = CHIMES_SRCDIR + "../build/chimes_lsq.py"
CHIMES_POSTPRC= CHIMES_SRCDIR + "../build/post_proc_chimes_lsq.py"


##HPC Settings
#########################
HPC_ACCOUNT = "TG-CHM240010"
HPC_PYTHON  = "/scratch/projects/compilers/intel24.0/oneapi/intelpython/python3.9/bin/python"
HPC_SYSTEM  = "TACC"
HPC_PPN     = 48 #for spr it has 112, for skx its 48
#HPC_EMAIL   = True
#EMAIL_ADD   = "aoladipupo@umich.edu"
# Generic weight settings

WEIGHTS_FORCE =   1.0

REGRESS_ALG   = "dlasso"
REGRESS_VAR   = "1.0E-5"
REGRESS_NRM   = True

N_HYPER_SETS  = 2
# Job submitting settings (avoid defaults because they will lead to long queue times)

CHIMES_BUILD_NODES = 1
CHIMES_BUILD_QUEUE = "skx"
CHIMES_BUILD_TIME  = "01:00:00"

CHIMES_SOLVE_NODES = 1
CHIMES_SOLVE_QUEUE = "skx"
CHIMES_SOLVE_TIME  = "01:00:00"
CHIMES_LSQ_MODULES = "intel/24.0 impi/21.11"

################################
##### Molecular Dynamics
################################

MD_STYLE        = "LMP"
MD_QUEUE          = ["skx"]*NO_CASES
MD_TIME           = ["1:00:00"]*NO_CASES
MD_NODES          = [1]*NO_CASES
MDFILES          = WORKING_DIR + "/ALL_BASE_FILES/LMPMD_BASEFILES/"
MD_MPI            = "/work2/09982/aoladipupo/stampede3/codes/chimes_calculator-LLfork/etc/lmp/exe/lmp_mpi_chimes"
MOLANAL         = CHIMES_SRCDIR + "../contrib/molanal/src/"
MOLANAL_SPECIES = ["C1"]

################################
##### Single-Point QM
################################
BULK_QM_METHOD = "LMP"
IGAS_QM_METHOD = "LMP" # Must be defined, even if unused
QM_FILES       = WORKING_DIR + "ALL_BASE_FILES/LMP_BASEFILES"

LMP_EXE      = "/work2/09982/aoladipupo/stampede3/codes/chimes_calculator-LLfork/etc/lmp/exe/lmp_mpi_chimes" # Has class2 compiled in it
LMP_UNITS    = "REAL"
LMP_TIME     = "00:10:00"
LMP_NODES    = 1
LMP_PPN      = 1
LMP_MEM      = 48
LMP_QUEUE    = "skx"
LMP_MODULES  = "intel/24.0 impi/21.11"
