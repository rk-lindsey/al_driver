
################################
##### General options
################################

EMAIL_ADD = "lindsey11@llnl.gov"

ATOM_TYPES     = ["C"]
NO_CASES       = 1

DRIVER_DIR     = "/usr/WS2/rlindsey/al_driver-fork/"
WORKING_DIR    = "/usr/WS2/rlindsey/al_driver-fork/examples/simple_iter_single_statepoint/"
CHIMES_SRCDIR  = "/usr/WS2/rlindsey/al_driver-fork/chimes_lsq-forALD/src/"

################################
##### ChIMES LSQ
################################

ALC0_FILES    = WORKING_DIR + "ALL_BASE_FILES/ALC-0_BASEFILES/"
CHIMES_LSQ    = CHIMES_SRCDIR + "../build/chimes_lsq"
CHIMES_SOLVER = CHIMES_SRCDIR + "../build/chimes_lsq.py"
CHIMES_POSTPRC= CHIMES_SRCDIR + "../build/post_proc_chimes_lsq.py"

# Generic weight settings

WEIGHTS_FORCE =   1.0

REGRESS_ALG   = "dlasso"
REGRESS_VAR   = "1.0E-5"
REGRESS_NRM   = True

# Job submitting settings (avoid defaults because they will lead to long queue times)

CHIMES_BUILD_NODES = 2
CHIMES_BUILD_QUEUE = "pdebug"
CHIMES_BUILD_TIME  = "01:00:00"

CHIMES_SOLVE_NODES = 2
CHIMES_SOLVE_QUEUE = "pdebug"
CHIMES_SOLVE_TIME  = "01:00:00"

################################
##### Molecular Dynamics
################################

MD_STYLE        = "CHIMES"
CHIMES_MD_MPI   = CHIMES_SRCDIR + "../build/chimes_md"

MOLANAL         = CHIMES_SRCDIR + "../contrib/molanal/src/"
MOLANAL_SPECIES = ["C1"]

################################
##### Single-Point QM
################################

QM_FILES = WORKING_DIR + "ALL_BASE_FILES/QM_BASEFILES"
VASP_EXE = "/usr/gapps/emc-vasp/vasp.5.4.4/build/gam/vasp"
VASP_TIME    = "01:00:00"
VASP_NODES   = 2
VASP_PPN     = 36
