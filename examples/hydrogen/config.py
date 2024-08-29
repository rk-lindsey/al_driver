

"""

	A configuration file containing all user-specified parameters.
	
	Notes: Relative paths will almost certainly break the code.
	
"""

################################
##### General variables
################################

EMAIL_ADD     = "salzaim@umich.edu" # driver will send updates on the status of the current run ... If blank (""), no emails are sent

SEED          = 1
ATOM_TYPES    = ["H"]
NO_CASES      = 2

# Cases:
# 300K_0.1gcc
# 2000K_0.2gcc


MOLANAL_SPECIES = ["H"]
		   
USE_AL_STRS   = 0     # A cycle number. 
STRS_STYLE    = "ALL" # Options: "DIAG" or "ALL"

DRIVER_DIR    = "/p/lustre1/fmatchDB/for_Safa/al_driver-LLfork-main-2_editedKpts/"
WORKING_DIR   = "/p/lustre2/alzaim1/ALD_tester/"
CHIMES_SRCDIR = "/p/lustre1/alzaim1/chimes_lsq-LLfork/"


HPC_PYTHON="/usr/tce/bin/python3"
HPC_ACCOUNT = "iap"



################################
##### ChIMES LSQ
################################

ALC0_FILES    = WORKING_DIR + "ALL_BASE_FILES/ALC-0_BASEFILES/"
CHIMES_LSQ    = CHIMES_SRCDIR + "build/chimes_lsq"
CHIMES_SOLVER = CHIMES_SRCDIR + "build/chimes_lsq.py"
CHIMES_POSTPRC= CHIMES_SRCDIR + "build/post_proc_chimes_lsq.py"

WEIGHTS_FORCE = [ ["A","B"], [[1.0  ],[1.0,-1.0]] ] #   1.0
WEIGHTS_FGAS  = [ ["A","B"], [[1.0  ],[1.0,-1.0]] ] #   1.0
WEIGHTS_ENER  = [ ["A","B"], [[1.0  ],[1.0,-1.0]] ] #   0.1
WEIGHTS_EGAS  = [ ["A","B"], [[1.00 ],[1.0,-1.0]] ] #   1.0
WEIGHTS_STRES = [ ["A","B"], [[100.0 ],[1.0,-1.0]] ] # 100.0

REGRESS_ALG   = "dlasso"
REGRESS_VAR   = "1.0E-8" # For 2-body, can't get below ~1.0E-7
REGRESS_NRM   = True

CHIMES_BUILD_NODES = 1
CHIMES_BUILD_QUEUE = "pdebug"
CHIMES_BUILD_TIME  = "1:00:00"

CHIMES_SOLVE_NODES = 1
CHIMES_SOLVE_QUEUE = "pdebug"
CHIMES_SOLVE_TIME  = "1:00:00"

CHIMES_LSQ_MODULES = "cmake/3.21.1 intel/18.0.1 impi/2018.0 mkl"

################################
##### Molecular Dynamics
################################

MD_STYLE     = "CHIMES"
CHIMES_MD_MPI = CHIMES_SRCDIR + "build/chimes_md-mpi"
CHIMES_MD_SER = CHIMES_SRCDIR + "build/chimes_md-serial"
CHIMES_MOLANAL= "/g/g17/rlindsey/CURR_TRACKED-GEN/contrib/molanlal/"
MDFILES= WORKING_DIR + "ALL_BASE_FILES/CHIMESMD_BASEFILES/"

CHIMES_PEN_PREFAC = 1.0E6
CHIMES_PEN_DIST   = 0.02

MD_NODES = [1, 2] # [4] *NO_CASES # 4 nodes for all jobs
MD_QUEUE = ["pdebug",  "pdebug"] # ["pbatch"]*NO_CASES # pbatch queue for all
MD_TIME  = ["1:00:00", "1:00:00"] # ["4:00:00"]*NO_CASES # 4 hour walltime for all

MOLANAL         = CHIMES_SRCDIR + "contrib/molanal/src/"
MOLANAL_SPECIES = ["H1"]

################################
##### Single-Point QM
################################

QM_FILES = WORKING_DIR + "ALL_BASE_FILES/QM_BASEFILES"
VASP_EXE = "/p/lustre1/fmatchDB/for_Safa/vaspnew/vasp.5.4.4.pl2/bin/vasp_gam"
VASP_QUEUE = "pdebug"
VASP_TIME    = "01:00:00"
VASP_NODES   = [10, 15]
VASP_PPN     = 50
VASP_MODULES = "intel-classic/2021.6.0-magic mkl-interfaces/2022.1.0 mkl/2022.1.0 mvapich2/2.3.7"

