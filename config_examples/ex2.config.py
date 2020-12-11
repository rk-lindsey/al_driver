"""

	A configuration file containing all user-specified parameters.
	
	Notes: Relative paths will almost certainly break the code.
	
"""


################################
# Set user specified variables 
################################

#WARNING: This code probably won't work if you use relative paths!

##### General variables

EMAIL_ADD     = "lindsey11@llnl.gov" # driver will send updates on the status of the current run ... If blank (""), no emails are sent

SEED          = 1

ATOM_TYPES    = ["C", "O"]
NO_CASES      = 3

# All cycles after and including USE_AL_STRS will include stress tensors for full self-consisitently obtained frames
# Note that for ALC 0, whether stress tensors are included is determined by the settings in config.ALC0_FILES/fm_setup.in
# If no stress tensors are desired, set to False (case sensitive)

USE_AL_STRS   = 2 # A cycle number. 

# This controls how stress tensors are included. DIAG means only the 3 diagonal components will be taken. "ALL" means all 6 unique components are taken.
STRS_STYLE    = "DIAG" # Options: "DIAG" or "ALL"

# This parmeter controls which INCAR file is grabbed for VASP calculations. Jobs will use <SMEARING TEMP>.INCAR. If no value is specified, 
# will use the temperature from the correspoding case in the traj_list file. Assumes case and traj_list.dat ordering match!

THIS_SMEAR    = None       # See comment above

# FYI:
#
# CASE-0: 2400 K; 1.79 gcc
# CASE-1: 6500 K; 2.50 gcc 
# CASE-2: 9350 K; 2.56 gcc


DRIVER_DIR    = "/usr/WS2/rlindsey/ChIMES4B_SVN/contrib/AL_driver/"	# This driver's src location
WORKING_DIR   = DRIVER_DIR + "/tests/CASES-3_SOLVER-DLASSO_MATRIX-SINGLE_FIT-F+E_diff_Tele/run_test/"	# Directory from which all ALCs will be run
CHIMES_SRCDIR = "/usr/workspace/wsb/rlindsey/ChIMES4B_SVN/src/"		# Location of ChIMES src files ... expects also post_proc_lsq2.py there


##### General HPC options

HPC_PPN       = 36
HPC_ACCOUNT   = "pbronze"
HPC_SYSTEM    = "slurm"
HPC_PYTHON    = "/usr/tce/bin/python"
HPC_EMAIL     = True # Adds "MSUB -m abe" to slurm scripts


##### ChIMES LSQ

ALC0_FILES    = WORKING_DIR + "ALL_BASE_FILES/ALC-0_BASEFILES/"

CHIMES_LSQ    = CHIMES_SRCDIR + "chimes_lsq"
CHIMES_SOLVER = CHIMES_SRCDIR + "lsq2.py"
CHIMES_POSTPRC= CHIMES_SRCDIR + "post_proc_lsq2.py"

WEIGHTS_FORCE = 1.0 
WEIGHTS_ENER  = 5.0
WEIGHTS_STRES = 500.0

REGRESS_ALG   = "dlasso" # "lassolars"
REGRESS_VAR   = "1.0E-4"

CHIMES_BUILD_NODES = 2
CHIMES_BUILD_QUEUE = "pdebug"
CHIMES_BUILD_TIME  = "00:30:00"		# Hours

CHIMES_SOLVE_NODES = 4
CHIMES_SOLVE_QUEUE = "pbatch" # "pdebug"
CHIMES_SOLVE_TIME  = "01:00:00" # "01:00:00" "00:30:00"	# Hours


##### ChIMES MD

CHIMES_MD      = CHIMES_SRCDIR + "chimes_md"
CHIMES_MOLANAL= "/g/g17/rlindsey/CURR_TRACKED-GEN/contrib/molanlal/"  
CHIMES_MDFILES= WORKING_DIR + "ALL_BASE_FILES/CHIMESMD_BASEFILES/"

CHIMES_PEN_PREFAC = 1.0E6
CHIMES_PEN_DIST   = 0.02

CHIMES_MD_NODES = 8
CHIMES_MD_QUEUE = "pbatch"
CHIMES_MD_TIME  = "03:00:00"		# Hours

############### added for the independent md runs #######################
CHIMES_MD_TIME_LIST = ["00:10:00", "01:00:00", "02:00:00", "02:00:00"]
ALC_LIST = [1, 5]
CASES_LIST = [0, 1, 2, 3]
INDEP_LIST = [1, 2, 3, 4, 5]
########################################################################


##### Cluster specific paths/variables

DO_CLUSTER    = True
TIGHT_CRIT    = WORKING_DIR + "ALL_BASE_FILES/tight_bond_crit.dat"
LOOSE_CRIT    = WORKING_DIR + "ALL_BASE_FILES/loose_bond_crit.dat"
CLU_CODE      = DRIVER_DIR  + "/utilities/new_ts_clu.cpp"


##### ALC-specific variables ... Note: Hardwired for partial memory mode

MEM_BINS = 40
MEM_CYCL = MEM_BINS/10
MEM_NSEL = 400
MEM_ECUT = 100.0

CALC_REPO_ENER_CENT_QUEUE = "pdebug" # added
CALC_REPO_ENER_CENT_TIME = "00:10:00"

CALC_REPO_ENER_QUEUE = "pbatch"
CALC_REPO_ENER_TIME  = "01:30:00" # modified: 4


##### VASP Specific variables

VASP_FILES   = WORKING_DIR + "ALL_BASE_FILES/VASP_BASEFILES"
VASP_POSTPRC = CHIMES_SRCDIR + "vasp2xyzf.py"
VASP_NODES   = 6
VASP_TIME    = "00:30:00"
VASP_QUEUE   = "pdebug"
VASP_EXE     = "/usr/gapps/emc-vasp/vasp.5.4.1/build/std/vasp"
VASP_MODULES = "mkl" # Currently unused, but should be included



