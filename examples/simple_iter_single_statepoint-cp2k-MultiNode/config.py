# Configred for SiOH with DFT(CP2K) run on UT-TACC (Stampede3) by Sayed Ahmad Almohri

################################
##### General options
################################

ATOM_TYPES     = ["Si","O"]
NO_CASES       = 3

DRIVER_DIR     = "/work2/09982/aalmohri/stampede3/Codes/al_driver-MyLLfork_dev/"
WORKING_DIR    = "/scratch/09982/aalmohri/TestNodeALD/2024-10-09-C-DiffNodes/"
CHIMES_SRCDIR  = "/work2/09982/aalmohri/stampede3/Codes/chimes_lsq-MyLLfork/src/"

################################
#### HPC Settings
################################

HPC_ACCOUNT = "TG-CHM240010"
HPC_PYTHON  = "/scratch/projects/compilers/intel24.0/oneapi/intelpython/python3.9/bin/python"
HPC_SYSTEM  = "TACC"
HPC_PPN     = 80 #for spr it has 112, for skx its 48
HPC_EMAIL   = True
EMAIL_ADD   = "aalmohri@umich.edu"

################################
##### ChIMES LSQ
################################

ALC0_FILES    = WORKING_DIR + "ALL_BASE_FILES/ALC-0_BASEFILES/"
CHIMES_LSQ    = CHIMES_SRCDIR + "../build/chimes_lsq"
CHIMES_SOLVER = CHIMES_SRCDIR + "../build/chimes_lsq.py"
CHIMES_POSTPRC= CHIMES_SRCDIR + "../build/post_proc_chimes_lsq.py"
CHIMES_MODULES= "intel/24.0 impi/21.11 "
# Generic weight settings

WEIGHTS_FORCE = [ ["A","B"], [[1.0  ],[1.0,-1.0]] ] #   1.0
WEIGHTS_FGAS  = [ ["A","B"], [[1.0  ],[1.0,-1.0]] ] #   1.0
WEIGHTS_ENER  = [ ["A","B"], [[0.1  ],[1.0,-1.0]] ] #   0.1
WEIGHTS_EGAS  = [ ["A","B"], [[1.0  ],[1.0,-1.0]] ] #   1.0
WEIGHTS_STRES = [ ["A","B"], [[100.0],[1.0,-1.0]] ] # 100.0

# Regression settings

REGRESS_ALG   = "dlasso"
REGRESS_VAR   = "1.0E-5"
REGRESS_NRM   = True
USE_AL_STRS   = 142134 #Use a large number so that we do not fit to stresses

# Penalty Prefactor


# Job submitting settings (avoid defaults because they will lead to long queue times)

CHIMES_BUILD_NODES = 1
CHIMES_BUILD_QUEUE = "icx"
CHIMES_BUILD_TIME  = "09:00:00"

CHIMES_SOLVE_NODES = 1
CHIMES_SOLVE_QUEUE = "icx"
CHIMES_SOLVE_TIME  = "09:00:00"
CHIMES_LSQ_MODULES = CHIMES_MODULES

CHIMES_PEN_PREFAC = 1.0E5 # Default is 1.0E6 I am lowering it to have smoother kicks

################################
##### Molecular Dynamics
################################
MD_STYLE          = "CHIMES"
MD_QUEUE          = ["icx"]*NO_CASES
MD_TIME           = ["10:00:00"]*NO_CASES
CHIMES_MD_MPI     = CHIMES_SRCDIR + "../build/chimes_md"
CHIMES_MD_MODULES = CHIMES_MODULES
MD_NODES          = [1]*NO_CASES

MOLANAL         = CHIMES_SRCDIR + "../contrib/molanal/src/"
MOLANAL_SPECIES = ["O1","Si1","H1"]

################################
##### Single-Point QM
################################

BULK_QM_METHOD = "CP2K"
IGAS_QM_METHOD = "CP2K" # Must be defined, even if unused

QM_FILES     = WORKING_DIR + "ALL_BASE_FILES/QM_BASEFILES"
CP2K_EXE     = "/work2/09982/aalmohri/stampede3/software/bin/cp2k.psmp"
CP2K_TIME    = "10:00:00"
CP2K_NODES   = [2, 1, 3]
CP2K_PPN     = 80
#CP2K_MEM     = 144
CP2K_QUEUE   = "icx"
CP2K_MODULES = "intel/24.0 impi/21.11 "
CP2K_DATADIR = "/work2/09982/aalmohri/stampede3/software/cp2k/data/"
