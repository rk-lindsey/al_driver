# Configred for seamless run on UM-ARC (Great Lakes)

################################
##### General options
################################

ATOM_TYPES     = ["Si","O"]
NO_CASES       = 1

DRIVER_DIR     = "/home/rklinds/codes/al_driver-myLLfork"
WORKING_DIR    = "/nfs/turbo/coe-rklinds/test_cp2k/bulk_MFI/temp_1000K-compr_0perc-shear_0deg/test_ald/"
CHIMES_SRCDIR  = "/home/rklinds/codes/chimes_lsq-myLLfork/src/"

################################
#### HPC Settings
################################

HPC_ACCOUNT = "rklinds1"
HPC_PYTHON  = "/sw/pkgs/arc/python3.9-anaconda/2021.11/bin/python"

################################
##### ChIMES LSQ
################################

ALC0_FILES    = WORKING_DIR + "ALL_BASE_FILES/ALC-0_BASEFILES/"
CHIMES_LSQ    = CHIMES_SRCDIR + "../build/chimes_lsq"
CHIMES_SOLVER = CHIMES_SRCDIR + "../build/chimes_lsq.py"
CHIMES_POSTPRC= CHIMES_SRCDIR + "../build/post_proc_chimes_lsq.py"
CHIMES_MODULES= "intel/2022.1.2 impi/2021.5.1 mkl/2022.0.2 "

# Generic weight settings

WEIGHTS_FORCE =   1.0
WEIGHTS_ENER  =   1.0

REGRESS_ALG   = "dlasso"
REGRESS_VAR   = "1.0E-5"
REGRESS_NRM   = True

# Job submitting settings (avoid defaults because they will lead to long queue times)

CHIMES_BUILD_NODES = 1
CHIMES_BUILD_QUEUE = "standard"
CHIMES_BUILD_TIME  = "01:00:00"

CHIMES_SOLVE_NODES = 1
CHIMES_SOLVE_QUEUE = "standard"
CHIMES_SOLVE_TIME  = "01:00:00"
CHIMES_LSQ_MODULES = CHIMES_MODULES

################################
##### Molecular Dynamics
################################

MD_STYLE          = "CHIMES"
MD_QUEUE          = ["standard"]*NO_CASES
MD_TIME           = ["00:03:00"]*NO_CASES
CHIMES_MD_MPI     = CHIMES_SRCDIR + "../build/chimes_md"
CHIMES_MD_MODULES = CHIMES_MODULES

MOLANAL         = CHIMES_SRCDIR + "../contrib/molanal/src/"
MOLANAL_SPECIES = ["O1","Si1"]

################################
##### Single-Point QM
################################

BULK_QM_METHOD = "CP2K"
IGAS_QM_METHOD = "CP2K" # Must be defined, even if unused

QM_FILES     = WORKING_DIR + "ALL_BASE_FILES/QM_BASEFILES"
CP2K_EXE     = "/nfs/turbo/coe-rklinds/software/cp2k/exe/Linux-intel-x86_64-RKL/cp2k.popt"
CP2K_TIME    = "01:00:00"
CP2K_NODES   = 2
CP2K_PPN     = 36
CP2K_MEM     = 128 
CP2K_QUEUE   = "standard"
CP2K_MODULES = "intel/2022.1.2 impi/2021.5.1 mkl/2022.0.2"
CP2K_DATADIR = "/nfs/turbo/coe-rklinds/software/cp2k/data/"

