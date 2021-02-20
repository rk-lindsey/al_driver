# Global (python) modules

import os
import sys

def print_help():

	"""
	
	Prints a list of expected config options and thier purpose"
	
	"""

	PARAM.append("EMAIL_ADD");                      VARTYP.append("str");           DETAILS.append("E-mail address for driver to sent status updates to")
	PARAM.append("SEED");                           VARTYP.append("int");           DETAILS.append("Seed for random number generator (used for MC cluster selection)")
	PARAM.append("ATOM_TYPES");                     VARTYP.append("str list");      DETAILS.append("List of atom types in system of interest , e.g. [\"C\", \"H\", \"O\", \"N\"]")
	PARAM.append("NO_CASES");                       VARTYP.append("int");           DETAILS.append("Number of different state points considered")
	PARAM.append("MOLANAL_SPECIES");                VARTYP.append("str list");      DETAILS.append("List of species to track in molanal output, e.g. [\"C1 O1 1(O-C)\", \"C1 O2 2(O-C)\"] ")
	PARAM.append("STRS_STYLE");                     VARTYP.append("int");           DETAILS.append("ALC at which to start including stress tensors from ALC generated configrations ")
	PARAM.append("USE_AL_STRS");                    VARTYP.append("str");           DETAILS.append("How stress tensors should be included in the fit, e.g. \"DIAG\" or \"ALL\"")
	PARAM.append("THIS_SMEAR");                     VARTYP.append("float");         DETAILS.append("Thermal smearing T in K; if \"None\", different values are used for each case, set in the ALL_BASE_FILES traj_list.dat")
	PARAM.append("DRIVER_DIR");                     VARTYP.append("str");           DETAILS.append("Path to the al_driver code")
	PARAM.append("WORKING_DIR");                    VARTYP.append("str");           DETAILS.append("Path to directory in which code is being run")
	PARAM.append("CHIMES_SRCDIR");                  VARTYP.append("str");           DETAILS.append("Path to directory containing the ChIMES_MD source code")
	PARAM.append("HPC_PPN");                        VARTYP.append("int");           DETAILS.append("The number of processors per node on the machine code is launched on")
	PARAM.append("HPC_ACCOUNT");                    VARTYP.append("str");           DETAILS.append("Charge bank name on machine code is launched on (e.g. \"pbronze\")")
	PARAM.append("HPC_SYSTEM");                     VARTYP.append("str");           DETAILS.append("Job scheduler on machine code is launched on (only \"slurm\" is supported currently)")
	PARAM.append("HPC_PYTHON");                     VARTYP.append("str");           DETAILS.append("Path to python executable (2.X required for now)")
	PARAM.append("HPC_EMAIL");                      VARTYP.append("bool");          DETAILS.append("Controls whether driver status updates are e-mailed to user")
	PARAM.append("ALC0_FILES");                     VARTYP.append("str");           DETAILS.append("Path to base files required by the driver (e.g. ChIMES input files, VASP, input files, etc.)")
	PARAM.append("CHIMES_LSQ");                     VARTYP.append("str");           DETAILS.append("ChIMES_lsq executable absolute path (e.g. CHIMES_SRCDIR + \"chimes_lsq\")")
	PARAM.append("CHIMES_SOLVER");                  VARTYP.append("str");           DETAILS.append("lsq2.py executable absolute path (e.g. CHIMES_SRCDIR + \"lsq2.py\")")
	PARAM.append("CHIMES_POSTPRC");                 VARTYP.append("str");           DETAILS.append("post_proc_lsq2.py executable absolute path (e.g. CHIMES_SRCDIR + \"post_proc_lsq2.py\")")
	PARAM.append("WEIGHTS_FORCE");                  VARTYP.append("float");         DETAILS.append("Weight to apply to bulk forces during A-matrix solution ")
	PARAM.append("WEIGHTS_FGAS");                   VARTYP.append("float");         DETAILS.append("Weight to apply to gas forces during A-matrix solution")
	PARAM.append("WEIGHTS_ENER");                   VARTYP.append("float");         DETAILS.append("Weight to apply to bulk energies during A-matrix solution")
	PARAM.append("WEIGHTS_EGAS");                   VARTYP.append("float");         DETAILS.append("Weight to apply to gas energies during A-matrix solution")
	PARAM.append("WEIGHTS_STRES");                  VARTYP.append("float");         DETAILS.append("Weight to apply to stress tensor components during A-matrix solution")
	PARAM.append("REGRESS_ALG");                    VARTYP.append("str");           DETAILS.append("Regression algorithm to use for fitting; only \"lassolars\" supported for now")
	PARAM.append("REGRESS_NRM");                    VARTYP.append("bool");          DETAILS.append("Controls whether A-matrix is normalized prior to solution")
	PARAM.append("REGRESS_VAR");                    VARTYP.append("bool");          DETAILS.append("Regression regularization variable")
	PARAM.append("CHIMES_BUILD_NODES");             VARTYP.append("int");           DETAILS.append("Number of nodes to use when running chimes_lsq")
	PARAM.append("CHIMES_BUILD_QUEUE");             VARTYP.append("int");           DETAILS.append("Queue to submit chimes_lsq job to")
	PARAM.append("CHIMES_BUILD_TIME");              VARTYP.append("str");           DETAILS.append("Walltime for chimes_lsq job (e.g. \"04:00:00\")")
	PARAM.append("CHIMES_SOLVE_NODES");             VARTYP.append("int");           DETAILS.append("Number of nodes to use when running lsq2.py/DLARS (lassolars)")
	PARAM.append("CHIMES_SOLVE_QUEUE");             VARTYP.append("str");           DETAILS.append("Queue to submit the lsq2.py/DLARS (lassolars) job to")
	PARAM.append("CHIMES_SOLVE_TIME");              VARTYP.append("str");           DETAILS.append("Walltime for lsq2.py/DLARS (lassolars) job (e.g. \"04:00:00\")")
	PARAM.append("CHIMES_MD_ser");                  VARTYP.append("str");           DETAILS.append("Serial ChIMES_md executable absolute path (e.g. CHIMES_SRCDIR + \"chimes_md-serial\")")
	PARAM.append("CHIMES_MD_MPI");                  VARTYP.append("str");           DETAILS.append("MPI-compatible ChIMES_md exectuable absolute path (e.g. CHIMES_SRCDIR + \"chimes_md-mpi\")")
	PARAM.append("CHIMES_MOLANAL");                 VARTYP.append("str");           DETAILS.append("Absolute path to the molanal src directory")
	PARAM.append("CHIMES_MDFILES");                 VARTYP.append("str");           DETAILS.append("Absolute path to ChIMES_MD input files like case-0.indep-0.run_md.in (e.g. WORKING_DIR + \"ALL_BASE_FILES/CHIMESMD_FILES\")")
	PARAM.append("CHIMES_PEN_PREFAC");              VARTYP.append("float");         DETAILS.append("ChIMES penalty function prefactor")
	PARAM.append("CHIMES_PEN_DIST");                VARTYP.append("float");         DETAILS.append("ChIMES pentalty function kick-in distance")
	PARAM.append("CHIMES_MD_NODES");                VARTYP.append("int");           DETAILS.append("Number of nodes to use when running chimes_md")
	PARAM.append("CHIMES_MD_QUEUE");                VARTYP.append("str");           DETAILS.append("Queue to submit chimes_md to")
	PARAM.append("CHIMES_MD_TIME");                 VARTYP.append("str");           DETAILS.append("Walltime for chimes_md (e.g. \"04:00:00\")")
	PARAM.append("DO_CLUSTER");                     VARTYP.append("bool");          DETAILS.append("If false, AL-driver only considers bulk configurations. Otherwise, cluster extraction, etc. is performed")
	PARAM.append("MAX_CLUATM");                     VARTYP.append("int");           DETAILS.append("Maximum number of atoms a cluster is allowed to contain (ignores clusters with more atoms)")
	PARAM.append("TIGHT_CRIT");                     VARTYP.append("str");           DETAILS.append("Absolute path to tight cutoff criteria file for clustering")
	PARAM.append("LOOSE_CRIT");                     VARTYP.append("str");           DETAILS.append("Absolute path to loose cutoff criteria file for clustering")
	PARAM.append("CLU_CODE");                       VARTYP.append("str");           DETAILS.append("Absolute path the clustering executable (compiled from utilities/new_ts_cluster.cpp)")
	PARAM.append("MEM_BINS");                       VARTYP.append("int");           DETAILS.append("Number of bins to use during cluster selection")
	PARAM.append("MEM_CYCL");                       VARTYP.append("int");           DETAILS.append("Number of MC cycles to use during cluster selection")
	PARAM.append("MEM_NSEL");                       VARTYP.append("int");           DETAILS.append("Number of clusters to select")
	PARAM.append("MEM_ECUT");                       VARTYP.append("float");         DETAILS.append("Maximum ChIMES \"dumb\" energy cutoff for cluster selection")
	PARAM.append("CALC_REPO_ENER_CENT_QUEUE");      VARTYP.append("str");           DETAILS.append("Queue to submit cluster ChIMES \"dumb\" energy calculations for central repository clusters to")
	PARAM.append("CALC_REPO_ENER_CENT_TIME");       VARTYP.append("str");           DETAILS.append("Walltime for ChIMES \"dumb\" energy calculations for central repository clusters")
	PARAM.append("CALC_REPO_ENER_QUEUE");           VARTYP.append("str");           DETAILS.append("Queue to submit cluster ChIMES \"dumb\" energy calculations for candidate clusters to")
	PARAM.append("CALC_REPO_ENER_TIME");            VARTYP.append("str");           DETAILS.append("Walltime for ChIMES \"dumb\" energy calculations for candidate clusters")
	PARAM.append("BULK_QM_METHOD");                 VARTYP.append("str");           DETAILS.append("Specifies which nominal QM code to use for bulk configurations; options are \"VASP\" or \"DFTB+\"")
	PARAM.append("IGAS_QM_METHOD");                 VARTYP.append("str");           DETAILS.append("Specifies which nominal QM code to use for gas configurations; options are \"VASP\", \"DFTB+\", and \"Gaussian\"")
	PARAM.append("VASP_FILES");                     VARTYP.append("str");           DETAILS.append("Absolute path to VASP input files")
	PARAM.append("VASP_POSTPRC");                   VARTYP.append("str");           DETAILS.append("Absolute path to vasp2yzf.py ")
	PARAM.append("VASP_NODES");                     VARTYP.append("int");           DETAILS.append("Number of nodes to use for VASP jobs")
	PARAM.append("VASP_PPN");                       VARTYP.append("int");           DETAILS.append("Number of processors to use per node for VASP jobs")
	PARAM.append("VASP_TIME");                      VARTYP.append("str");           DETAILS.append("Walltime for VASP calculations, e.g. \"04:00:00\"")
	PARAM.append("VASP_QUEUE");                     VARTYP.append("str");           DETAILS.append("Queue to submit VASP jobs to")
	PARAM.append("VASP_EXE");                       VARTYP.append("str");           DETAILS.append("Absolute path to VASP executable")
	PARAM.append("DFTB_FILES");                     VARTYP.append("str");           DETAILS.append("Absolute path to DFTB+ input file ")
	PARAM.append("DFTB_POSTPRC");                   VARTYP.append("str");           DETAILS.append("Absolute path to dftb+2yzf.py ")
	PARAM.append("DFTB_NODES");                     VARTYP.append("int");           DETAILS.append("Number of nodes to use for DFTB+ jobs")
	PARAM.append("DFTB_PPN");                       VARTYP.append("int");           DETAILS.append("Number of processors to use per node for DFTB+ jobs")
	PARAM.append("DFTB_TIME");                      VARTYP.append("str");           DETAILS.append("Walltime for DFTB+ calculations, e.g. \"04:00:00\"")
	PARAM.append("DFTB_QUEUE");                     VARTYP.append("str");           DETAILS.append("Queue to submit DFTB+ jobs to")
	PARAM.append("DFTB_EXE");                       VARTYP.append("str");           DETAILS.append("Absolute path to DFTB+ executable")
	PARAM.append("GAUS_NODES");                     VARTYP.append("int");           DETAILS.append("Number of nodes to use for Gaussian jobs")
	PARAM.append("GAUS_TIME");                      VARTYP.append("str");           DETAILS.append("Walltime for Gaussian calculations, e.g. \"04:00:00\"")
	PARAM.append("GAUS_QUEUE");                     VARTYP.append("str");           DETAILS.append("Queue to submit Gaussian jobs to")
	PARAM.append("GAUS_EXE");                       VARTYP.append("str");           DETAILS.append("Absolute path to Gaussian executable")
	PARAM.append("GAUS_SCR");                       VARTYP.append("str");           DETAILS.append("Absolute path to Gaussian scratch directory")


	print "Help info: "
	print "Run with, e.g.: unbuffer python /path/to/al_driver/main.py 0 1 2 | tee driver.log"
	print "This tool is best launched from a screen session, which allows the determinal to be detached"
	print "Config file options are:"

	for i in xrange(len(PARAM)):
	        print PARAM[i] + '\t' + VARTYP[i] + '\t' + DETAILS[i] + '\n'

	print ""
	
	return	
	

def verify(user_config):

	"""
	
	Checks whether config.py has been properly specified.
	Produces warnings for un-initialized values and interactively
	allows the user to either use a default or enter the desired value.
	
	Usage: verify(user_config)
	
	"""
	
	################################
	##### General variables
	################################

	if not hasattr(user_config,'EMAIL_ADD'):
		
		# Used by the Driver to send updates on the status of the current run 
		# If blank (""), no emails are sent.

		print "WARNING: Option config.EMAIL_ADD was not set"
		print "         Will not send e-mail updates. " 
		

	if not hasattr(user_config,'SEED'):

		# A seed for random selections

		print "WARNING: Option config.SEED was not set"
		print "         Will use a value of 1"	
		
		user_config.SEED          = 1
		

	if not hasattr(user_config,'ATOM_TYPES'):

		# The number of atom types to consider

		print "ERROR: Option config.ATOM_TYPES was not set"
		print "       Acceptable settings are of the form: [\"C\", \"N\" ,\"O\"]"	
		
		exit()
		
	if not hasattr(user_config,'NO_CASES'):

		# The number of cases (state points) to consider

		print "ERROR: Option config.NO_CASES was not set"
		print "       Acceptable settings are of the form of an integer	"
		
		exit()	

	if not hasattr(user_config,'MOLANAL_SPECIES'):

		# Species to track/plot from molanal... only used for post-processing

		MOLANAL_SPECIES = ["C1 O1 1(O-C)",
	                   "C1 O2 2(O-C)",
	                   "N2 1(N-N)",
	                   "N1 O1 1(O-N)",
			   "N2 O1 1(N-N) 1(O-N)",
			   "O2 1(O-O)"]

		print "WARNING: Option config.MOLANAL_SPECIES was not set"
		print "         Will use:"
		print "\t",MOLANAL_SPECIES
		
		user_config.MOLANAL_SPECIES = MOLANAL_SPECIES

	if not hasattr(user_config,'USE_AL_STRS'):

	       # All cycles after and including USE_AL_STRS will include stress tensors for full self-consisitently obtained frames 
	       # Note that for ALC 0, whether stress tensors are included is determined by the settings in config.ALC0_FILES/fm_setup.in 
	       # If no stress tensors are desired, set to False (case sensitive)

		print "WARNING: Option config.USE_AL_STRS was not set"
		print "         Will use a value of 5"
		
		user_config.USE_AL_STRS = 5

	if not hasattr(user_config,'STRS_STYLE'):

	       # This controls how stress tensors are included. DIAG means only the 3 diagonal components will be taken. 
	       # "ALL" means all 6 unique components are taken.
	       
		print "WARNING: Option config.STRS_STYLE was not set"
		print "         Will use \"ALL\" (i.e. rather than \"DIAG\")"

		user_config.STRS_STYLE    = "ALL"

	if not hasattr(user_config,'THIS_SMEAR'):

		# This parmeter controls which INCAR file is grabbed for VASP calculations. Jobs will use <SMEARING TEMP>.INCAR. If no value is specified, 
		# will use the temperature from the correspoding case in the traj_list file. Assumes case and traj_list.dat ordering match!
		
		print "WARNING: Option config.THIS_SMEAR was not set"
		print "         Will assume values are provided in the traj_list file, in K"

		user_config.THIS_SMEAR = None       # See comment above
		

	if not hasattr(user_config,'DRIVER_DIR'):

		# This driver's src location
		
		print "ERROR: Option config.DRIVER_DIR was not set"
		print "       Acceptable settings are of the form of an absolute path (Unix)"
		
		exit()
		
	if not hasattr(user_config,'WORKING_DIR'):

		# Directory from which all ALCs will be run
		
		print "ERROR: Option config.WORKING_DIR was not set"
		print "       Acceptable settings are of the form of an absolute path (Unix)"
		
		exit()	
		
	if not hasattr(user_config,'CHIMES_SRCDIR'):

		# Location of ChIMES src files ... expects also post_proc_lsq2.py there
		
		print "ERROR: Option config.CHIMES_SRCDIR was not set"
		print "       Acceptable settings are of the form of an absolute path (Unix)"
		
		exit()

	################################
	##### General HPC options
	################################



	if not hasattr(user_config,'HPC_PPN'):

		# Number of procs per node

		print "WARNING: Option config.HPC_PPN was not set"
		print "         Will use a value of 36"	
		
		user_config.HPC_PPN = 36
		
	if not hasattr(user_config,'HPC_ACCOUNT'):

		# HPC Charge bank/account

		print "WARNING: Option config.HPC_ACCOUNT was not set"
		print "         Will use pbronze"	
		
		user_config.HPC_ACCOUNT = "pbronze"	
		
	if not hasattr(user_config,'HPC_SYSTEM'):

		# HPC System (i.e. SLURM, Torque, etc.)

		print "WARNING: Option config.HPC_SYSTEM was not set"
		print "         Will use slurm"
		print "		Note: No other options are currently supported."	
		
		user_config.HPC_SYSTEM = "slurm"	

		
	if not hasattr(user_config,'HPC_PYTHON'):

		# Path to python executable

		print "WARNING: Option config.HPC_PYTHON was not set"
		print "         Will use /usr/tce/bin/python"
		print "		Note: This script currently requires python2.x"	
		
		user_config.HPC_PYTHON = "/usr/tce/bin/python"	
		
	if not hasattr(user_config, 'HPC_EMAIL'):

		# Boolean: Have the HPC system send job status emails?

		print "WARNING: Option config.HPC_EMAIL was not set"
		print "         Will use True"
		
		user_config.HPC_EMAIL = True


	################################
	##### ChIMES LSQ
	################################
	
	if not hasattr(user_config,'ALC0_FILES'):

		# Location of ALC-0 base files

		print "WARNING: Option config.ALC0_FILES was not set"
		print "         Will use config.WORKING_DIR + \"ALL_BASE_FILES/ALC-0_BASEFILES/\""
		
		user_config.ALC0_FILES = user_config.WORKING_DIR + "ALL_BASE_FILES/ALC-0_BASEFILES/"

	if not hasattr(user_config,'CHIMES_LSQ'):

		# Location of chimes_lsq executable

		print "WARNING: Option config.CHIMES_LSQ was not set"
		print "         Will use config.CHIMES_SRCDIR + \"chimes_lsq\""
		
		user_config.CHIMES_LSQ    = user_config.CHIMES_SRCDIR + "chimes_lsq"

	if not hasattr(user_config,'CHIMES_SOLVER'):

		# Location of lsq2.py script

		print "WARNING: Option config.CHIMES_SOLVER was not set"
		print "         Will use config.CHIMES_SRCDIR + \"lsq2.py\""
		
		user_config.CHIMES_SOLVER = user_config.CHIMES_SRCDIR + "lsq2.py"
		
	if not hasattr(user_config,'CHIMES_POSTPRC'):

		# Location of post_proc_lsq2.py script

		print "WARNING: Option config.CHIMES_POSTPRC was not set"
		print "         Will use config.CHIMES_SRCDIR + \"post_proc_lsq2.py\""
		
		user_config.CHIMES_SOLVER = user_config.CHIMES_SRCDIR + "post_proc_lsq2.py"
		
	if not hasattr(user_config,'WEIGHTS_FORCE'):

		# Weights for bulk frame forces

		print "WARNING: Option config.WEIGHTS_FORCE was not set"
		print "         Will use a value of 1.0"
		
		user_config.WEIGHTS_FORCE = 1.0	
		
	if not hasattr(user_config,'WEIGHTS_FGAS'):

		# Weights for gas frame forces
		
		# Notes on WEIGHTS_FGAS: If positive, a single weight value is used. Otherwise, values are automatically set to
		# -WEIGHTS_FGAS/<natoms in cluster>, where W_FGAS is should be max atoms in the training traj 

		print "WARNING: Option config.WEIGHTS_FGAS was not set"
		print "         Will use a value of 5.0"
		
		user_config.WEIGHTS_FGAS = 5.0							

	if not hasattr(user_config,'WEIGHTS_ENER'):

		# Weights for bulk frame energies

		print "WARNING: Option config.WEIGHTS_ENER was not set"
		print "         Will use a value of 0.1"
		
		user_config.WEIGHTS_ENER = 0.1	
		
	
	if not hasattr(user_config,'WEIGHTS_EGAS'):

		# Weights for gas frame energies

		print "WARNING: Option config.WEIGHTS_EGAS was not set"
		print "         Will use a value of 0.1"
		
		user_config.WEIGHTS_EGAS = 0.1
		
	if not hasattr(user_config,'WEIGHTS_STRES'):

		# Weights for stress tensor components

		print "WARNING: Option config.WEIGHTS_STRES was not set"
		print "         Will use a value of 250.0"
		
		user_config.WEIGHTS_STRES = 250.0

	if not hasattr(user_config,'REGRESS_ALG'):

		# What regression algorithm should be used?

		print "WARNING: Option config.REGRESS_ALG was not set"
		print "         Will use dlasso"
		
		user_config.REGRESS_ALG = "dlasso"
		
	if not hasattr(user_config,'REGRESS_NRM'):

		# Should the regression algorithm normalize the problem first?

		print "WARNING: Option config.REGRESS_NRM was not set"
		print "         Will use a value of True"
		
		user_config.REGRESS_NRM = True	# Note: Default behavior is true!
		
	if not hasattr(user_config,'REGRESS_VAR'):

		# The regression regularization variable

		print "WARNING: Option config.REGRESS_VAR was not set"
		print "         Will use a value of 1.0E-5"
		
		user_config.REGRESS_VAR = 1.0E-5				

	if not hasattr(user_config,'CHIMES_BUILD_NODES'):

		# The number of nodes to use for chimes_lsq

		print "WARNING: Option config.CHIMES_BUILD_NODES was not set"
		print "         Will use a value of 4"
		
		user_config.CHIMES_BUILD_NODES = 4

	if not hasattr(user_config,'CHIMES_BUILD_QUEUE'):

		# The queue to submit the chimes_lsq job to

		print "WARNING: Option config.CHIMES_BUILD_QUEUE was not set"
		print "         Will use pbatch"
		
		user_config.CHIMES_BUILD_QUEUE = "pbatch"
		
	if not hasattr(user_config,'CHIMES_BUILD_TIME'):

		# How long the job should be submitted for (hours)

		print "WARNING: Option config.CHIMES_BUILD_TIME was not set"
		print "         Will use \"04:00:00\""
		
		user_config.CHIMES_BUILD_TIME = "04:00:00"		

	if not hasattr(user_config,'CHIMES_SOLVE_NODES'):

		# The number of nodes to use when solving the design matrix

		print "WARNING: Option config.CHIMES_SOLVE_NODES was not set"
		print "         Will use a value of 12"
		
		user_config.CHIMES_SOLVE_NODES = 12

	if not hasattr(user_config,'CHIMES_SOLVE_QUEUE'):

		# The queue to use when solving the design matrix

		print "WARNING: Option config.CHIMES_SOLVE_QUEUE was not set"
		print "         Will use pbatch"
		
		user_config.CHIMES_SOLVE_QUEUE = "pbatch"


	if not hasattr(user_config,'CHIMES_SOLVE_TIME'):

		# How long the job should be submitted for (hours)
		
		# Pre-split capability:
		# Note: 8 nodes//8 hours worked for all up to ALC 6
		# Increasing to 12 nodes for ALC 6
		# ability to read from split files could help in the future...
		# 
		# Post-split capability:
		# on ALC-7, have a ~800 Gb a-mat. Splitting across 8 nodes (288 procs)
		# takes ~30 min (unweighted), and solving takes ~2 hours. MUCH more efficient! :)

		print "WARNING: Option config.CHIMES_SOLVE_TIME was not set"
		print "         Will use \"24:00:00\""
		
		user_config.CHIMES_SOLVE_TIME = "24:00:00"

	################################
	##### ChIMES MD
	################################
	
	if hasattr(user_config,'CHIMES_MD'):

		# Path to chimes_md executable

		print "WARNING: Defunct option config.CHIMES_MD was set"
		print "         Ignoring. Will search for config.CHIMES_MD_SER and config.CHIMES_MD_MPI"
		
	if not hasattr(user_config,'CHIMES_MD_SER'):

		# Path to the serial chimes_md executable

		print "WARNING: Option config.CHIMES_MD_SER was not set"
		print "         Will use config.CHIMES_SRCDIR + \"chimes_md-serial\""
		
		user_config.CHIMES_MD_SER = user_config.CHIMES_SRCDIR + "chimes_md-serial"		
		
	if not hasattr(user_config,'CHIMES_MD_MPI'):

		# Path to chimes_md executable

		print "WARNING: Option config.CHIMES_MD_MPI was not set"
		print "         Will use config.CHIMES_SRCDIR + \"chimes_md-mpi\""
		
		user_config.CHIMES_MD_MPI = user_config.CHIMES_SRCDIR + "chimes_md-mpi"		
		
	if not hasattr(user_config,'CHIMES_MOLANAL'):

		# Path to molanal executable

		print "Error: Option config.CHIMES_MOLANAL was not set"
		print "       Acceptable settings are of the form of an absolute path (Unix)"
		
		exit()
		
	if not hasattr(user_config,'CHIMES_MDFILES'):

		# Path to the base chimes_md files (i.e. input.xyz's and run_md.in's)

		print "WARNING: Option config.CHIMES_MDFILES was not set"
		print "         Will use config.WORKING_DIR + \"ALL_BASE_FILES/CHIMESMD_BASEFILES/\""
		
		user_config.CHIMES_MD = user_config.WORKING_DIR + "ALL_BASE_FILES/CHIMESMD_BASEFILES/"

	if not hasattr(user_config,'CHIMES_PEN_PREFAC'):

		# Penalty function prefactor

		print "WARNING: Option config.CHIMES_PEN_PREFAC was not set"
		print "         Will use a value of 1.0E6"
		
		user_config.CHIMES_PEN_PREFAC = 1.0E6
		
	if not hasattr(user_config,'CHIMES_PEN_DIST'):

		# Penalty function kick-in distance

		print "WARNING: Option config.CHIMES_PEN_DIST was not set"
		print "         Will use a value of 0.02"
		
		user_config.CHIMES_PEN_DIST = 0.02		

	if not hasattr(user_config,'CHIMES_MD_NODES'):

		# Number of nodes to use for MD jobs

		print "WARNING: Option config.CHIMES_MD_NODES was not set"
		print "         Will use a value of 8"
		
		user_config.CHIMES_MD_NODES = 8	
		
	if not hasattr(user_config,'CHIMES_MD_QUEUE'):

		# Queue to use for MD jobs

		print "WARNING: Option config.CHIMES_MD_QUEUE was not set"
		print "         Will use pbatch"
		
		user_config.CHIMES_MD_QUEUE = "pbatch"	
		
	if not hasattr(user_config,'CHIMES_MD_TIME'):

		# Time to request for MD jobs (hours)

		print "WARNING: Option config.CHIMES_MD_TIME was not set"
		print "         Will use a value of \"4:00:00\""
		
		user_config.CHIMES_MD_TIME = "4:00:00"			

	################################
	##### Cluster specific paths/variables
	################################

	if not hasattr(user_config,'DO_CLUSTER'):

		# Should cluster extraction/use be performed?
		# ... I don't think "False" is actually implemented yet... 

		print "WARNING: Option config.DO_CLUSTER was not set"
		print "         Will use a value of True"
		print "		Note: \"False\" is not current supported"
		
		user_config.DO_CLUSTER = True

	if not hasattr(user_config,'MAX_CLUATM'):

		# Max number of atoms to consider in a cluster

		print "WARNING: Option config.MAX_CLUATM was not set"
		print "         Will use a value of 100"

		user_config.MAX_CLUATM = 100
		 	
	if not hasattr(user_config,'TIGHT_CRIT'):

		# File with tight clustering criteria

		print "WARNING: Option config.TIGHT_CRIT was not set"
		print "         Will use config.WORKING_DIR + \"ALL_BASE_FILES/tight_bond_crit.dat\""

		user_config.TIGHT_CRIT = user_config.WORKING_DIR + "ALL_BASE_FILES/tight_bond_crit.dat"
		
	if not hasattr(user_config,'LOOSE_CRIT'):

		# File with loose clustering criteria... if set equal to the tight criteria file,
		# then no "loose" (i.e. "ts") clusters are generated.

		print "WARNING: Option config.LOOSE_CRIT was not set"
		print "         Will use config.WORKING_DIR + \"ALL_BASE_FILES/loose_bond_crit.dat\""

		user_config.LOOSE_CRIT = user_config.WORKING_DIR + "ALL_BASE_FILES/loose_bond_crit.dat"		
		
	if not hasattr(user_config,'CLU_CODE'):

		# Cluster extraction code

		print "WARNING: Option config.CLU_CODE was not set"
		print "         Will use config.DRIVER_DIR  + \"/utilities/new_ts_clu.cpp\""

		user_config.CLU_CODE = user_config.DRIVER_DIR  + "/utilities/new_ts_clu.cpp"
				

	################################
	##### ALC-specific variables ... Note: Hardwired for partial memory mode
	################################

	if not hasattr(user_config,'MEM_BINS'):

		# number of bins for histograms (cluster selection)

		print "WARNING: Option config.MEM_BINS was not set"
		print "         Will use a value of 40"

		user_config.MEM_BINS = 40	
	
	if not hasattr(user_config,'MEM_CYCL'):

		# number of cycles for cluster selection

		print "WARNING: Option config.MEM_CYCL was not set"
		print "         Will use a value of config.MEM_BINS/10"

		user_config.MEM_CYCL = user_config.MEM_BINS/10		
	
	if not hasattr(user_config,'MEM_NSEL'):

		# number of clusters to select each ALC

		print "WARNING: Option config.MEM_NSEL was not set"
		print "         Will use a value of 400"

		user_config.MEM_NSEL = 400
		
	if not hasattr(user_config,'MEM_ECUT'):

		# Energy cutoff (E/atom in kcal/mol) cutoff for cluster selection

		print "WARNING: Option config.MEM_ECUT was not set"
		print "         Will use a value of 100.0"

		user_config.MEM_ECUT = 100.0		
		
	if not hasattr(user_config,'CALC_REPO_ENER_CENT_QUEUE'):

		# Queue for central repo energy calculations

		print "WARNING: Option config.CALC_REPO_ENER_CENT_QUEUE was not set"
		print "         Will use pbatch"

		user_config.CALC_REPO_ENER_CENT_QUEUE = "pdebug"
		
	if not hasattr(user_config,'CALC_REPO_ENER_CENT_TIME'):

		# Time for central repo energy calculations

		print "WARNING: Option config.CALC_REPO_ENER_CENT_TIME was not set"
		print "         Will use a value of \"00:10:00\""

		user_config.CALC_REPO_ENER_CENT_TIME =  "00:10:00"	
		
	if not hasattr(user_config,'CALC_REPO_ENER_QUEUE'):

		# Queue for central repo energy calculations

		print "WARNING: Option config.CALC_REPO_ENER_QUEUE was not set"
		print "         Will use pbatch"

		user_config.CALC_REPO_ENER_QUEUE = "pbatch"
		
	if not hasattr(user_config,'CALC_REPO_ENER_TIME'):

		# Time for central repo energy calculations

		print "WARNING: Option config.CALC_REPO_ENER_TIME was not set"
		print "         Will use a value of \"04:00:00\""

		user_config.CALC_REPO_ENER_TIME =  "04:00:00"				
			

	################################
	##### QM-Specific variables
	################################

	if not hasattr(user_config,'BULK_QM_METHOD'):

		# Software/method for calculating Forces/stresses/energies for bulk configurations
		# Currently only VASP is supported, but CP2K should be included in the future

		print "WARNING: Option config.BULK_QM_METHOD was not set"
		print "         Will use VASP"

		user_config.BULK_QM_METHOD = "VASP"
		
	if not hasattr(user_config,'IGAS_QM_METHOD'):

		# Software/method for calculating Forces/stresses/energies for gas configurations
		# Currently, can also use "Gaussian... requires assignment of additional vars, checked below
		#
		# Note that if Gaussian is used, single-atom-energy offsets are hardcoded currentlly (see process_gaussian.py)
		# NWChem should be added in the future

		print "WARNING: Option config.IGAS_QM_METHOD was not set"
		print "         Will use VASP"

		user_config.IGAS_QM_METHOD = "VASP"		


	if ((user_config.BULK_QM_METHOD == "VASP") or (user_config.IGAS_QM_METHOD == "VASP")):
	
		if not hasattr(user_config,'VASP_FILES'):

			# Location of basic VASP input files (INCAR, KPOINTS, etc)

			print "WARNING: Option config.VASP_FILES was not set"
			print "         Will use config.WORKING_DIR + \"ALL_BASE_FILES/VASP_BASEFILES\""

			user_config.VASP_FILES = user_config.WORKING_DIR + "ALL_BASE_FILES/VASP_BASEFILES"
			
		if not hasattr(user_config,'VASP_POSTPRC'):

			# Location of a vasp post-processing file ... this should really be in a process_vasp.py file...

			print "WARNING: Option config.VASP_POSTPRC was not set"
			print "         Will use config.CHIMES_SRCDIR + \"vasp2xyzf.py\""

			user_config.VASP_POSTPRC = user_config.CHIMES_SRCDIR + "vasp2xyzf.py"			
			
		if not hasattr(user_config,'VASP_NODES'):

			# Number of nodes to use for a VASP calculation

			print "WARNING: Option config.VASP_NODES was not set"
			print "         Will use a value of 6"

			user_config.VASP_NODES = 6
			
		if not hasattr(user_config,'VASP_PPN'):

			# Number of nodes to use for a VASP calculation

			print "WARNING: Option config.VASP_PPN was not set"
			print "         Will use a value of 36"

			user_config.VASP_NODES = 36							

		if not hasattr(user_config,'VASP_TIME'):

			# Time for a VASP calculation (hrs)

			print "WARNING: Option config.VASP_TIME was not set"
			print "         Will use a value of \"04:00:00\""

			user_config.VASP_TIME = "04:00:00"
			
		if not hasattr(user_config,'VASP_QUEUE'):

			# Queue for a VASP calculation

			print "WARNING: Option config.VASP_QUEUE was not set"
			print "         Will use pbatch"

			user_config.VASP_QUEUE = "pbatch"
			
		if not hasattr(user_config,'VASP_EXE'):

			# VASP executable

			print "ERROR: Option config.VASP_EXE was not set"
			print "         Acceptable settings are of the form: \"/path/to/vasp.exe\""
			
			exit()
			
	if ((user_config.BULK_QM_METHOD == "DFTB+") or (user_config.IGAS_QM_METHOD == "DFTB+")):
	
		if not hasattr(user_config,'DFTB_FILES'):

			# Location of basic DFTB+ input files (dftb_in.hsd)

			print "WARNING: Option config.DFTB_FILES was not set"
			print "         Will use config.WORKING_DIR + \"ALL_BASE_FILES/QM_BASEFILES\""

			user_config.VASP_FILES = user_config.WORKING_DIR + "ALL_BASE_FILES/QM_BASEFILES"
			
		if not hasattr(user_config,'DFTB_POSTPRC'):

			# Location of a dftb+ post-processing file ... this should really be in a process_dftb.py file...

			print "WARNING: Option config.DFTB_POSTPRC was not set"
			print "         Will use config.CHIMES_SRCDIR + \"dftb+2xyzf.py\""

			user_config.DFTB_POSTPRC = user_config.CHIMES_SRCDIR + "dftb+2xyzf.py"			
			
		if not hasattr(user_config,'DFTB_NODES'):

			# Number of nodes to use for a DFTB calculation

			print "WARNING: Option config.DFTB_NODES was not set"
			print "         Will use a value of 1"

			user_config.DFTB_NODES = 1
			
		if not hasattr(user_config,'DFTB_PPN'):

			# Number of nodes to use for a DFTB calculation

			print "WARNING: Option config.DFTB_PPN was not set"
			print "         Will use a value of 1"

			user_config.DFTB_NODES = 1							

		if not hasattr(user_config,'DFTB_TIME'):

			# Time for a DFTB calculation (hrs)

			print "WARNING: Option config.DFTB_TIME was not set"
			print "         Will use a value of \"04:00:00\""

			user_config.DFTB_TIME = "04:00:00"
			
		if not hasattr(user_config,'DFTB_QUEUE'):

			# Queue for a DFTB calculation

			print "WARNING: Option config.DFTB_QUEUE was not set"
			print "         Will use pbatch"

			user_config.DFTB_QUEUE = "pbatch"
			
		if not hasattr(user_config,'DFTB_EXE'):

			# DFTB+ executable

			print "ERROR: Option config.DFTB_EXE was not set"
			print "         Acceptable settings are of the form: \"/path/to/dftbplus.exe\""
			
			exit()
			

	if user_config.IGAS_QM_METHOD == "Gaussian":

		#if not hasattr(user_config,'GAUS_POSTPRC'): -- this option is unused
		#
		#	# Number of nodes to use for a Gaussian calculation
		#
		#	print "WARNING: Option config.GAUS_POSTPRC was not set"
		#	print "         Will use config.CHIMES_SRCDIR + \"/contrib/gaussian2xyzf.py\""
		#
		#	user_config.GAUS_POSTPRC = config.CHIMES_SRCDIR + "/contrib/gaussian2xyzf.py"			

		if not hasattr(user_config,'GAUS_NODES'):

			# Number of nodes to use for a Gaussian calculation

			print "WARNING: Option config.GAUS_NODES was not set"
			print "         Will use a value of 4"

			user_config.GAUS_NODES = 4				

		if not hasattr(user_config,'GAUS_TIME'):

			# Time for a Gaussian calculation (hrs)

			print "WARNING: Option config.GAUS_TIME was not set"
			print "         Will use a value of \"04:00:00\""

			user_config.GAUS_TIME = "04:00:00"
			
		if not hasattr(user_config,'GAUS_QUEUE'):

			# Queue for a Gaussian calculation

			print "WARNING: Option config.GAUS_QUEUE was not set"
			print "         Will use pbatch"

			user_config.GAUS_QUEUE = "pbatch"
			
		if not hasattr(user_config,'GAUS_EXE'):

			# Gaussian executable

			print "ERROR: Option config.GAUS_EXE was not set"
			print "         Acceptable settings are of the form: \"/path/to/gaussian.exe\""
			
			exit()
			
		if not hasattr(user_config,'GAUS_SCR'):

			# Gaussian scratch space

			print "ERROR: Option config.GAUS_SCR was not set"
			print "         Acceptable settings are of the form: \"/path/to/gaussian/scratch/space\""
			
			exit()			

