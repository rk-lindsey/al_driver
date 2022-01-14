
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
		   

USE_AL_STRS   = 6 # A cycle number. 
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

WEIGHTS_FORCE =    1.0 
WEIGHTS_FGAS  =  -66.0 # Changed to -264/4 = -66 # Changed to -264/2 = -132 from -264.0 bc gas forces were over-weighted
WEIGHTS_ENER  =    0.5
WEIGHTS_EGAS  =    0.1
WEIGHTS_STRES =  250.0

REGRESS_ALG   = "dlasso" # "lassolars"
REGRESS_VAR   = "1.0E-5"
REGRESS_NRM   = True    # Note: Default behavior is true!!!!

CHIMES_BUILD_NODES = 4
CHIMES_BUILD_QUEUE = "pbatch"
CHIMES_BUILD_TIME  = "04:00:00"		# Hours

CHIMES_SOLVE_NODES = 12
CHIMES_SOLVE_QUEUE = "pbatch" # "pdebug"
CHIMES_SOLVE_TIME  = "24:00:00" # "08:00:00" # "01:00:00" "00:30:00"	# Hours

################################
##### ChIMES MD
################################

CHIMES_MD_MPI = CHIMES_SRCDIR + "chimes_md-mpi"
CHIMES_MD_SER = CHIMES_SRCDIR + "chimes_md-serial"  # Executable for serial chimes_md compilation (i.e. using g++ rather than mpicxx)
CHIMES_MOLANAL= "/g/g17/rlindsey/CURR_TRACKED-GEN/contrib/molanlal/"  
CHIMES_MDFILES= WORKING_DIR + "ALL_BASE_FILES/CHIMESMD_BASEFILES/"

CHIMES_PEN_PREFAC = 1.0E6
CHIMES_PEN_DIST   = 0.02

CHIMES_MD_NODES = 8
CHIMES_MD_QUEUE = "pbatch"
CHIMES_MD_TIME  = "4:00:00"		# Hours

DO_CLUSTER    = True
MAX_CLUATM    = 100 # Maximum number of atoms to allow in a cluster
TIGHT_CRIT    = WORKING_DIR + "ALL_BASE_FILES/tight_bond_crit.dat"
LOOSE_CRIT    = WORKING_DIR + "ALL_BASE_FILES/loose_bond_crit.dat"
CLU_CODE      = DRIVER_DIR  + "/utilities/new_ts_clu.cpp"

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
##### QM-Specific variables
################################

# ***** NEW VARIABLES AS OF 06/19/20 ***** #

BULK_QM_METHOD = "VASP"     # Currently supported options are "VASP" and "DFTB+"... coming soon-ish: CP2K
IGAS_QM_METHOD = "Gaussian" # Currently supported options are "VASP or Gaussian" ... coming soon-ish: NWChem

GAUS_NODES   = 4
GAUS_TIME    = "04:00:00"
GAUS_QUEUE   = "pbatch"
GAUS_EXE     = "/usr/WS1/compchem/gaussian/g16/g16" # Assumes user's environment is properly configured
GAUS_SCR     = "/usr/tmp/rlindsey/"

# ***** #

VASP_FILES   = WORKING_DIR + "ALL_BASE_FILES/VASP_BASEFILES"
VASP_POSTPRC = CHIMES_SRCDIR + "../contrib/vasp/vasp2xyzf.py"
VASP_NODES   = 6
VASP_TIME    = "04:00:00"
VASP_QUEUE   = "pbatch"
VASP_EXE     = "/usr/gapps/emc-vasp/vasp.5.4.1/build/std/vasp"
VASP_MODULES = "mkl" # Currently unused, but should be included

# ***** # 

DFTB_FILES   = VASP_FILES # For now the code assumes all QM-related input files are in the same location, set by VASP_FILES
DFTB_POSTPRC = CHIMES_SRCDIR + "../contrib/vasp/dftb+2xyzf.py" # This script can only process 1 frame at a time
DFTB_NODES   = 1
DFTB_PPN     = 1 
DFTB_TIME    = "04:00:00"
DFTB_QUEUE   = "pbatch"
DFTB_EXE     = "/usr/gapps/polymers/dftbplus-17.1/_build/prog/dftb+/dftb+"
DFTB_MODULES = "mkl" # Currently unused but should be, esp if thread parallism is requested




