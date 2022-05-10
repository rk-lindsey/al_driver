
"""

	A configuration file containing all user-specified parameters.
	
	Notes: Relative paths will almost certainly break the code.
	
"""

################################
##### General variables
################################

EMAIL_ADD     = "lindsey11@llnl.gov" # driver will send updates on the status of the current run ... If blank (""), no emails are sent

SEED          = 1

ATOM_TYPES    = ["C", "N" ,"O"]
NO_CASES      = 7

# FYI:
#
# CASE 1: 1.80gcc_383K;
# CASE 2: 1.86gcc_300K;
# CASE 3: 2.00gcc_2000K
# CASE 4: 2.00gcc_4250K
# CASE 5: 2.25gcc_4440K
# CASE 6: 2.50gcc_4700K
# CASE 7: 2.50gcc_9000K

MOLANAL_SPECIES = ["C1 O1 1(O-C)",
                   "C1 O2 2(O-C)",
                   "N2 1(N-N)",
                   "N1 O1 1(O-N)",
		   "N2 O1 1(N-N) 1(O-N)",
		   "O2 1(O-O)"]
		   

USE_AL_STRS   = 6 # A cycle number - include stresses for all cycles >= 6 
STRS_STYLE    = "ALL" # Options: "DIAG" or "ALL"

THIS_SMEAR    = None       # See comment above

DRIVER_DIR    = "/usr/workspace/wsb/rlindsey/al_driver_stable"	# This driver's src location
WORKING_DIR   = "/p/lustre2/rlindsey/DNTF_MODEL-7/"				# Directory from which all ALCs will be run
CHIMES_SRCDIR = "/usr/workspace/wsb/rlindsey/ChIMES4B_SVN/src/"			# Location of ChIMES src files ... expects also post_proc_lsq2.py there

################################
##### General HPC options
################################

HPC_PPN       = 36
HPC_ACCOUNT   = "pbronze"
HPC_SYSTEM    = "slurm"
HPC_PYTHON    = "/usr/tce/bin/python"
HPC_EMAIL     = True

################################
##### ChIMES LSQ
################################

ALC0_FILES    = WORKING_DIR + "ALL_BASE_FILES/ALC-0_BASEFILES/"

CHIMES_LSQ    = CHIMES_SRCDIR + "chimes_lsq"
CHIMES_SOLVER = CHIMES_SRCDIR + "lsq2.py"
CHIMES_POSTPRC= CHIMES_SRCDIR + "post_proc_lsq2.py"

# If set, ALC-0 (or 1, if cluster method isn't being used) weights
# are taken to be exactly those spcified in the WEIGHTS_ALC_0 

WEIGHTS_SET_ALC_0 = False
WEIGHTS_ALC_0     = ""

# Generic weight settings

WEIGHTS_FORCE = [ ["A","B"], [[1.0  ],[1.0,-1.0]]] #   1.0
WEIGHTS_FGAS  = [ ["A","B"], [[1.0  ],[1.0,-1.0]]] #   1.0
WEIGHTS_ENER  = [ ["A","B"], [[0.3  ],[1.0,-1.0]]] #        0.1
WEIGHTS_EGAS  = [ ["A","B"], [[1.0  ],[1.0,-1.0]]] #        1.0
WEIGHTS_STRES = [ ["A","B"], [[100.0],[1.0,-1.0]]] # 100.0

REGRESS_ALG   = "dlasso"


REGRESS_VAR   = "1.0E-8" # For 2-body, can't get below ~1.0E-7
REGRESS_NRM   = True

CHIMES_BUILD_NODES = 8
CHIMES_BUILD_QUEUE = "pdebug"
CHIMES_BUILD_TIME  = "00:60:00"

CHIMES_SOLVE_NODES = 8
CHIMES_SOLVE_QUEUE = "pdebug"
CHIMES_SOLVE_TIME  = "00:60:00"

################################
##### ChIMES-based MD
################################

MD_STYLE = "CHIMES"
DFTB_MD_SER   = None
CHIMES_MD_MPI = CHIMES_SRCDIR + "chimes_md-mpi"
CHIMES_MD_SER = CHIMES_SRCDIR + "chimes_md-serial"

MOLANAL  = "/g/g17/rlindsey/CURR_TRACKED-GEN/contrib/molanlal/"  
MDFILES  = WORKING_DIR + "ALL_BASE_FILES/CHIMESMD_BASEFILES/"

CHIMES_PEN_PREFAC = 1.0E6
CHIMES_PEN_DIST   = 0.02

MD_NODES = [4] *NO_CASES # 4 nodes for all jobs
MD_QUEUE = ["pbatch"]*NO_CASES # pbatch queue for all
MD_TIME  = ["4:00:00"]*NO_CASES # 4 hour walltime for all

################################
##### Cluster block
################################

DO_CLUSTER    = True
MAX_CLUATM    = 100 # Maximum number of atoms to allow in a cluster
TIGHT_CRIT    = WORKING_DIR + "ALL_BASE_FILES/tight_bond_crit.dat"
LOOSE_CRIT    = WORKING_DIR + "ALL_BASE_FILES/loose_bond_crit.dat"
CLU_CODE      = DRIVER_DIR  + "/utilities/new_ts_clu.cpp"

################################
##### Hierarchical fitting block
################################

# Note: Parameter files need to be in base files/hierarch
# Note: For each training traj config, need a corresponding temps file that gives the 
#       temperature for each frame
# Note: The base fm_setup.in should have # HIERARC # set true, and corresponding 1- and 2-body interactions excluded
# Note: Orders in the base fm_setup.in file should be greater or equal to those in the reference (HIERARCH_PARAM_FILES) files
# Note: TYPEIDX and PAIRIDX block info in the base fm_setup.in file needs to be correct with respect to the HIERARCH_PARAM_FILES
# Note: Ensure "SPECIAL XB" cutoffs are set to "SPECIFIC N", where N is the number of NON-excluded XB interaction types 

DO_HIERARCH = False
HIERARCH_PARAM_FILES = [] # ['C.params.txt.reduced', 'N.params.txt.reduced']
HIERARCH_EXE = None # CHIMES_MD_SER

################################
##### Correction fitting block
################################

# Note: If corrections are used, ChIMES_MD_{NODES,QUEUE,TIME} are all used to specify DFTB runs
# These should be renamed to "simulation_{...}" for the generalized MD block (which should become SIM block)
# Also, need to add a flag to run serial rather than requesting a whole node ... eh... can override in function

FIT_CORRECTION          = False
CORRECTED_TYPE          = None
CORRECTED_TYPE_FILES    = None
CORRECTED_TYPE_EXE      = None
CORRECTED_TEMPS_BY_FILE = None
# if true, temps in traj_list.dat ignored by correction FES subtraction. Instead, searches for <filesnames>.temps where .temps replaces whatever last extension was, in CORRECTED_TYPE_FILES

################################
##### ALC-specific variables ... Note: Hardwired for partial memory mode
################################

MEM_BINS = 40
MEM_CYCL = MEM_BINS/10
MEM_NSEL = 400
MEM_ECUT = 100.0 #  Set ATMENER false in run_md.cluster # 500.0 # Updated from 100 since now md code includes atom energy offsets

CALC_REPO_ENER_CENT_QUEUE = "pbatch" #"pdebug"
CALC_REPO_ENER_CENT_TIME = "4:00:00" # "00:10:00"

CALC_REPO_ENER_QUEUE =  "pbatch"
CALC_REPO_ENER_TIME  =  "4:00:00" 

################################
##### QM-Specific variables (Single point calculations)
################################

BULK_QM_METHOD = "VASP"     # Currently supported options are "VASP" and "DFTB+"... coming soon-ish: CP2K
IGAS_QM_METHOD = "Gaussian" # Currently supported options are "VASP or Gaussian" ... coming soon-ish: NWChem

QM_FILES = WORKING_DIR + "ALL_BASE_FILES/QM_BASEFILES"

# Gaussian-specific settings

GAUS_NODES   = 4
GAUS_TIME    = "04:00:00"
GAUS_QUEUE   = "pbatch"
GAUS_EXE     = "/usr/WS1/compchem/gaussian/g16/g16" # Assumes user's environment is properly configured
GAUS_SCR     = "/usr/tmp/rlindsey/"

# VASP-specific settings

VASP_FILES   = WORKING_DIR + "ALL_BASE_FILES/VASP_BASEFILES"
VASP_POSTPRC = CHIMES_SRCDIR + "../contrib/vasp/vasp2xyzf.py"
VASP_NODES   = 6
VASP_TIME    = "01:00:00"
VASP_QUEUE   = "pbatch"
VASP_EXE     = "/usr/gapps/emc-vasp/vasp.5.4.1/build/gam/vasp"
VASP_MODULES = "mkl" # Currently unused, but should be included

# DFTB-specific settings (unused for this study)

DFTB_FILES   = VASP_FILES # For now the code assumes all QM-related input files are in the same location, set by VASP_FILES
DFTB_POSTPRC = CHIMES_SRCDIR + "../contrib/vasp/dftb+2xyzf.py" # This script can only process 1 frame at a time
DFTB_NODES   = 1
DFTB_PPN     = 1 
DFTB_TIME    = "04:00:00"
DFTB_QUEUE   = "pbatch"
DFTB_EXE     = "/usr/gapps/polymers/dftbplus-17.1/_build/prog/dftb+/dftb+"
DFTB_MODULES = "mkl" # Currently unused but should be, esp if thread parallism is requested




