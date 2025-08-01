# Configured for seamless run on LLNL-LC (Quartz)

################################
##### General options
################################

ATOM_TYPES     = ["C"]
NO_CASES       = 1

DRIVER_DIR     = "/usr/WS2/rlindsey/test_cp2k/al_driver/"
WORKING_DIR    = "/usr/WS2/rlindsey/test_cp2k/al_driver/examples/simple_iter_single_statepoint/"
CHIMES_SRCDIR  = "/usr/WS2/rlindsey/test_cp2k/chimes_lsq/src/"
HPC_ACCOUNT    = "pbronze"

# Job submitting settings (avoid defaults because they will lead to long queue times)

CHIMES_BUILD_NODES = 2
CHIMES_BUILD_QUEUE = "pdebug"
CHIMES_BUILD_TIME  = "01:00:00"

CHIMES_SOLVE_NODES = 2
CHIMES_SOLVE_QUEUE = "pdebug"
CHIMES_SOLVE_TIME  = "01:00:00"

################################
##### ChIMES-MD 
################################

MD_QUEUE  = ["pbatch"] * NO_CASES
MD_NODES   = [2]*NO_CASES
MD_PPN     = [36]*NO_CASES
MD_TIME    = ["04:00:00"]*NO_CASES

################################
##### Single-Point QM
################################

VASP_EXE = "/usr/gapps/emc-vasp/vasp.5.4.4/build/gam/vasp"
VASP_QUEUE  = "pdebug"
VASP_TIME    = "01:00:00"
VASP_NODES   = 2
VASP_PPN     = 36
VASP_MODULES = "mkl intel/18.0.1 impi/2018.0"
