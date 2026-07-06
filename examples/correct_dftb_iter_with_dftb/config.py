# This test is a little silly.
# We generate a ChIMES model to correct DFTB.
# The initial training set is DFT.
# The siliness is that, during our iterations, we also use DFTB as the ground-truth QM method.
# You should never mix DFT and DFTB as a labeling method as we're doing here, and you should never train a ChIMES correction for DFTB to DFTB.
# This just exists to test functionality and show you how you might use some of these features. Be sure to read the comments below.
# This has been tested on the LLNL LC
# Verified for compatibility with DFTB+ development version (commit: 6ae315b4, base: 25.1)
# I *highly* recommend you run this in an interative session - otherwise the DFTB single points can be very slow. Also recommend running on a NFS-type file system
# e.g., salloc -N 1 -n 1 -t 60 -p pdebug 
#
# Run with: unbuffer python3 /path/to/main.py 0 1 2 | tee driver-0.log




################################
##### General options
################################

ATOM_TYPES     = ["N"]
NO_CASES       = 1
#STOP_AFTER     = Set this if you do not want to do any active learning. Options are SOLVE_AMAT" or "RUN_MD"

DRIVER_DIR     = "/usr/WS2/lindsey11/dftb_tests/al_driver/"
WORKING_DIR    = "/usr/WS2/lindsey11/dftb_tests/al_driver/examples/correct_dftb_iter_with_dftb/" 
CHIMES_SRCDIR  = "/usr/WS2/lindsey11/dftb_tests/chimes_lsq/src/"
DFTBPLUS_EXE   = "/usr/WS2/lindsey11/dftb_tests/dftbplus/installation/bin/dftb+"

################################
#### HPC Settings
################################

HPC_ACCOUNT = "iap"   # Adjust this for your system - this is the charge bank
HPC_PPN     = 8       # Just set it to a low number for this excersise

################################
##### ChIMES LSQ
################################

ALC0_FILES     = WORKING_DIR + "ALL_BASE_FILES/ALC-0_BASEFILES/"
CHIMES_LSQ     = CHIMES_SRCDIR + "../build/chimes_lsq"
CHIMES_SOLVER  = CHIMES_SRCDIR + "../build/chimes_lsq.py"
CHIMES_POSTPRC = CHIMES_SRCDIR + "../build/post_proc_chimes_lsq.py"
CHIMES_MODULES = "intel-classic/2021.6.0-magic mvapich2/2.3.7 mkl" # Adjust this for your system - these are the modules you use for ChIMES

# Generic weight settings

WEIGHTS_SET_ALC_0 = True
WEIGHTS_ALC_0     = ALC0_FILES + "/weights_comb.dat"

# Regression settings

REGRESS_ALG   = "dlasso"
REGRESS_VAR   = "1.0E-7"
REGRESS_NRM   = True

# Penalty Prefactor

CHIMES_PEN_PREFAC = 1000000.0
CHIMES_PEN_DIST   = 0.02

# Job submitting settings

CHIMES_BUILD_NODES = 1
CHIMES_BUILD_QUEUE = "pdebug"      # Adjust this, this is the queue to submit to
CHIMES_BUILD_TIME  = "00:05:00"

CHIMES_SOLVE_NODES = 1
CHIMES_SOLVE_QUEUE = "pdebug"      # Adjust this, this is the queue to submit to
CHIMES_SOLVE_TIME  = "00:30:00"
CHIMES_LSQ_MODULES = CHIMES_MODULES


################################
##### Molecular Dynamics
################################

MD_STYLE          = "DFTB+"
MD_FILES          = WORKING_DIR + "ALL_BASE_FILES/DFTBMD_BASEFILES/"
MD_QUEUE          = ["pdebug"]*NO_CASES
MD_TIME           = ["00:10:00"]*NO_CASES
MD_SER            = DFTBPLUS_EXE
MD_NODES          = [1]*NO_CASES
MD_OMPEXPORTS     = "export OMP_NUM_THREADS=4 OMP_PLACES=cores OMP_PROC_BIND=close" # Special flags to make DFTB calculations efficient

RUN_MOLANAL     = True
MOLANAL         = CHIMES_SRCDIR + "../contrib/molanal/src/"
MOLANAL_SPECIES = ["N1", "N2", "N3"]


################################
##### Correction fitting block - This is where we specify that we want to fit the ChIMES 
##### model to the difference between the ground truth (the .xyzf file in ALL_BASEFILES/ALC-0_BASEFILES, DFT in this case) and DFTB.
################################

# Note: if CORRECTED_TEMPS_BY_FILE true, temps in traj_list.dat ignored by correction FES subtraction. 
# Instead, searches for <filesnames>.temps where .temps replaces whatever last extension was, in 
# CORRECTED_TYPE_FILES. Temps in traj_list are still used for the MD step, however.


FIT_CORRECTION          = True
CORRECTED_TYPE          = "DFTB+"
CORRECTED_TYPE_FILES    = WORKING_DIR + "ALL_BASE_FILES/DFTBSP_BASEFILES/"
CORRECTED_TYPE_EXE      = DFTBPLUS_EXE
CORRECTED_TEMPS_BY_FILE = True 


################################
##### Single-Point QM -- This is where things get silly. The ALL_BASEFILES/ALC-0_BASEFILES/*.xyzf is DFT therefore this should 
##### also be the same DFT method. We're using DFTB here just for code testing purposes. 
################################

# Note: GEN FILENAME IN BASEFILE  MUST BE dftbjob.gen

BULK_QM_METHOD = "DFTB+"
IGAS_QM_METHOD = "DFTB+" # Must be defined, even if unused
QM_FILES       = WORKING_DIR + "ALL_BASE_FILES/DFTBSP_BASEFILES"   # UPDATE THE MANUAL TO GET RID OF THE DFTBFILES OPTION

DFTB_MEM       = 1
DFTB_NODES     = 1  
DFTB_PPN       = 1
DFTB_TIME      = "00:10:00"  
DFTB_QUEUE     = "pdebug"  
DFTB_EXE       = DFTBPLUS_EXE  
