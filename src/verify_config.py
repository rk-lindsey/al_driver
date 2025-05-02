# Global (python) modules

import os
import sys

def print_help():
 
    """
    
    Prints a list of expected config options and thier purpose"
    
    """
    PARAM=[]
    VARTYP=[]
    DETAILS=[]

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
    PARAM.append("DO_HIERARCH");                    VARTYP.append("bool");          DETAILS.append("Is this a hierarchical fit (i.e., building on existing parameters?") 
    PARAM.append("HIERARCH_PARAM_FILES");           VARTYP.append("str list");      DETAILS.append("List of parameter files to build on, which chould be in ALL_BASE_FILES/HIERARCH_PARAMS")     
    PARAM.append("HIERARCH_METHOD");                VARTYP.append("str");           DETAILS.append("MD method to use for subtracting existing parameter contributions - current options are CHIMES or LMP")     
    PARAM.append("HIERARCH_EXE");                   VARTYP.append("str");           DETAILS.append("Executable to use when subtracting existing parameter contributions")         
    PARAM.append("FIT_CORRECTION");                 VARTYP.append("bool");          DETAILS.append("Is this ChIMES model being fit as a correction to another method?") 
    PARAM.append("CORRECTED_TYPE");                 VARTYP.append("str");           DETAILS.append("Method type being corrected. Currently only \"DFTB\" is supported")    
    PARAM.append("CORRECTED_TYPE_FILES");           VARTYP.append("str");           DETAILS.append("Files needed to run simulations/single points with the method to be corrected")    
    PARAM.append("CORRECTED_TYPE_EXE");             VARTYP.append("str");           DETAILS.append("Executable to use when subtracting existing forces/energies/stresses from method to be corrected")    
    PARAM.append("CORRECTED_TEMPS_BY_FILE");        VARTYP.append("bool");          DETAILS.append("Should electron temperatures be set to values in traj_list.dat (false) or in specified file location, for correction calculation? Only needed if correction method is QM-based. ")
    PARAM.append("HPC_PPN");                        VARTYP.append("int");           DETAILS.append("The number of processors per node on the machine code is launched on")    
    PARAM.append("HPC_ACCOUNT");                    VARTYP.append("str");           DETAILS.append("Charge bank name on machine code is launched on (e.g. \"pbronze\")")
    PARAM.append("HPC_SYSTEM");                     VARTYP.append("str");           DETAILS.append("Job scheduler on machine code is launched on (only \"slurm\" , \"TACC\" and \"UM-ARC\" are supported currently)")
    PARAM.append("HPC_PYTHON");                     VARTYP.append("str");           DETAILS.append("Path to python executable (2.X required for now)")
    PARAM.append("HPC_EMAIL");                      VARTYP.append("bool");          DETAILS.append("Controls whether driver status updates are e-mailed to user")
    PARAM.append("ALC0_FILES");                     VARTYP.append("str");           DETAILS.append("Path to base files required by the driver (e.g. ChIMES input files, VASP, input files, etc.)")
    PARAM.append("CHIMES_LSQ");                     VARTYP.append("str");           DETAILS.append("ChIMES_lsq executable absolute path (e.g. CHIMES_SRCDIR + \"chimes_lsq\")")
    PARAM.append("CHIMES_SOLVER");                  VARTYP.append("str");           DETAILS.append("lsq2.py executable absolute path (e.g. CHIMES_SRCDIR + \"lsq2.py\")")
    PARAM.append("CHIMES_POSTPRC");                 VARTYP.append("str");           DETAILS.append("post_proc_lsq2.py executable absolute path (e.g. CHIMES_SRCDIR + \"post_proc_lsq2.py\")")
    PARAM.append("N_HYPER_SETS");                   VARTYP.append("int");           DETAILS.append("Number of unique fm_setup.in files; allows fitting, e.g., multiple overlapping models to the same data")
    PARAM.append("WEIGHTS_SET_ALC_0");              VARTYP.append("bool");          DETAILS.append("Should ALC-0 (or 1 if no clustering) weights be read directly from a user specified file? ")
    PARAM.append("WEIGHTS_ALC_0");                  VARTYP.append("str");           DETAILS.append("Set if WEIGHTS_SET_ALC_0 is true; path to user specified ALC-0 (or ALC-1) weights ")
    PARAM.append("WEIGHTS_FORCE");                  VARTYP.append("list");          DETAILS.append("Weight/method to apply to bulk forces during A-matrix solution ")
    PARAM.append("WEIGHTS_FGAS");                   VARTYP.append("list");          DETAILS.append("Weight/method to apply to gas forces during A-matrix solution")
    PARAM.append("WEIGHTS_ENER");                   VARTYP.append("list");          DETAILS.append("Weight/method to apply to bulk energies during A-matrix solution")
    PARAM.append("WEIGHTS_EGAS");                   VARTYP.append("list");          DETAILS.append("Weight/method to apply to gas energies during A-matrix solution")
    PARAM.append("WEIGHTS_STRES");                  VARTYP.append("list");          DETAILS.append("Weight/method to apply to stress tensor components during A-matrix solution")
    PARAM.append("REGRESS_ALG");                    VARTYP.append("str");           DETAILS.append("Regression algorithm to use for fitting; only \"lassolars\" supported for now")
    PARAM.append("REGRESS_NRM");                    VARTYP.append("bool");          DETAILS.append("Controls whether A-matrix is normalized prior to solution")
    PARAM.append("REGRESS_VAR");                    VARTYP.append("bool");          DETAILS.append("Regression regularization variable")
    PARAM.append("CHIMES_BUILD_NODES");             VARTYP.append("int");           DETAILS.append("Number of nodes to use when running chimes_lsq")
    PARAM.append("CHIMES_BUILD_QUEUE");             VARTYP.append("int");           DETAILS.append("Queue to submit chimes_lsq job to")
    PARAM.append("CHIMES_BUILD_TIME");              VARTYP.append("str");           DETAILS.append("Walltime for chimes_lsq job (e.g. \"04:00:00\")")
    PARAM.append("CHIMES_SOLVE_NODES");             VARTYP.append("int");           DETAILS.append("Number of nodes to use when running lsq2.py/DLARS (lassolars)")
    PARAM.append("CHIMES_SOLVE_PPN");               VARTYP.append("int");           DETAILS.append("Number of procs per node to use when running lsq2.py/DLARS (lassolars)")
    PARAM.append("CHIMES_SOLVE_QUEUE");             VARTYP.append("str");           DETAILS.append("Queue to submit the lsq2.py/DLARS (lassolars) job to")
    PARAM.append("CHIMES_SOLVE_TIME");              VARTYP.append("str");           DETAILS.append("Walltime for lsq2.py/DLARS (lassolars) job (e.g. \"04:00:00\")")
    PARAM.append("MD_STYLE");                       VARTYP.append("str");           DETAILS.append("Should MD simulations be run as ChIMES-only (\"CHIMES\") or DFTB+ChIMES (\"DFTB\")?")    
    PARAM.append("MOLANAL");                        VARTYP.append("str");           DETAILS.append("Absolute path to the molanal src directory")
    PARAM.append("MDFILES");                        VARTYP.append("str");           DETAILS.append("Absolute path to MD input files like case-0.indep-0.run_md.in (e.g. WORKING_DIR + \"ALL_BASE_FILES/CHIMESMD_FILES\")")
    PARAM.append("MD_NODES");                       VARTYP.append("int");           DETAILS.append("Number of nodes to use when running md simulations")
    PARAM.append("MD_QUEUE");                       VARTYP.append("str");           DETAILS.append("Queue to submit md simulations to to")
    PARAM.append("MD_TIME");                        VARTYP.append("str");           DETAILS.append("Walltime for md simulations (e.g. \"04:00:00\")")
    PARAM.append("DFTB_MD_SER");                    VARTYP.append("str");           DETAILS.append("DFTBplus executable absolute path")
    PARAM.append("CHIMES_MD_SER");                  VARTYP.append("str");           DETAILS.append("Serial ChIMES_md executable absolute path (e.g. CHIMES_SRCDIR + \"chimes_md-serial\")")
    PARAM.append("CHIMES_MD_MPI");                  VARTYP.append("str");           DETAILS.append("MPI-compatible ChIMES_md exectuable absolute path (e.g. CHIMES_SRCDIR + \"chimes_md-mpi\")")    
    PARAM.append("CHIMES_PEN_PREFAC");              VARTYP.append("float");         DETAILS.append("ChIMES penalty function prefactor")
    PARAM.append("CHIMES_PEN_DIST");                VARTYP.append("float");         DETAILS.append("ChIMES pentalty function kick-in distance")
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
    PARAM.append("QM_FILES");                       VARTYP.append("str");           DETAILS.append("Absolute path to QM input files")
    PARAM.append("VASP_POSTPRC");                   VARTYP.append("str");           DETAILS.append("Absolute path to vasp2yzf.py ")
    PARAM.append("VASP_NODES");                     VARTYP.append("int list");      DETAILS.append("Number of nodes to use for VASP jobs")
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
    PARAM.append("CP2K_NODES");                     VARTYP.append("int list");      DETAILS.append("Number of nodes to use for CP2K jobs")
    PARAM.append("CP2K_PPN");                       VARTYP.append("int");           DETAILS.append("Number of procs per node to use for CP2K jobs")
    PARAM.append("CP2K_TIME");                      VARTYP.append("str");           DETAILS.append("Walltime for CP2K calculations, e.g. \"04:00:00\"")
    PARAM.append("CP2K_QUEUE");                     VARTYP.append("str");           DETAILS.append("Queue to submit CP2K jobs to")
    PARAM.append("CP2K_EXE");                       VARTYP.append("str");           DETAILS.append("Absolute path to CP2K executable")
    PARAM.append("CP2K_DATADIR");                   VARTYP.append("str");           DETAILS.append("Absolute path to CP2K scratch (\"data\") directory")
    PARAM.append("GAUS_NODES");                     VARTYP.append("int");           DETAILS.append("Number of nodes to use for Gaussian jobs")
    PARAM.append("GAUS_PPN");                       VARTYP.append("int");           DETAILS.append("Number of procs per node to use for Gaussian jobs")
    PARAM.append("GAUS_TIME");                      VARTYP.append("str");           DETAILS.append("Walltime for Gaussian calculations, e.g. \"04:00:00\"")
    PARAM.append("GAUS_QUEUE");                     VARTYP.append("str");           DETAILS.append("Queue to submit Gaussian jobs to")
    PARAM.append("GAUS_EXE");                       VARTYP.append("str");           DETAILS.append("Absolute path to Gaussian executable")
    PARAM.append("GAUS_SCR");                       VARTYP.append("str");           DETAILS.append("Absolute path to Gaussian scratch directory")
    PARAM.append("GAUS_REF");                       VARTYP.append("str");           DETAILS.append("Name of file containing single atom energies from Gaussian and target planewave method")
    PARAM.append("LMP_FILES");                     VARTYP.append("int");           DETAILS.append("Path to input files if using it as a refernce (\"QM\") method")
    PARAM.append("LMP_NODES");                     VARTYP.append("int");           DETAILS.append("Number of nodes to use for LAMMPS jobs")
    PARAM.append("LMP_POSTPRC");                   VARTYP.append("str");           DETAILS.append("Path to lmp2xyz.py")
    PARAM.append("LMP_PPN");                       VARTYP.append("int");           DETAILS.append("Number of procs per node to use for LAMMPS jobs")
    PARAM.append("LMP_TIME");                      VARTYP.append("str");           DETAILS.append("Walltime for LAMMPS calculations, e.g. \"04:00:00\"")
    PARAM.append("LMP_QUEUE");                     VARTYP.append("str");           DETAILS.append("Queue to submit LAMMPS jobs to")
    PARAM.append("LMP_EXE");                       VARTYP.append("str");           DETAILS.append("Absolute path to LAMMPS executable")
    PARAM.append("LMP_MODULES");                    VARTYP.append("str");           DETAILS.append("System-specific modules needed to run LAMMPS")
    PARAM.append("LMP_DATADIR");                   VARTYP.append("str");           DETAILS.append("Absolute path to CP2K scratch (\"data\") directory")


    print("Help info: ")
    print("Run with, e.g.: unbuffer python /path/to/al_driver/main.py 0 1 2 | tee driver.log")
    print("This tool is best launched from a screen session, which allows the determinal to be detached")
    print("Config file options are:")

    for i in range(len(PARAM)):
            print(PARAM[i] + '\t' + VARTYP[i] + '\t' + DETAILS[i] + '\n')

    print("")
    
    return    
    
    
def check_VASP(user_config):    

    """
    
    Checks whether settings for VASP compatibility.
    Produces warnings for un-initialized values if VASP is requested
        
    Usage: check_VASP(user_config)
    
    """
        
    if not hasattr(user_config,'VASP_POSTPRC'):

        # Location of a vasp post-processing file ... this should really be in a process_vasp.py file...

        if ((user_config.BULK_QM_METHOD == "VASP") or (user_config.IGAS_QM_METHOD == "VASP")):
            print("WARNING: Option config.VASP_POSTPRC was not set")
            print("         Will use config.DRIVER_DIR + \"/src/vasp2xyzf.py\"")

        user_config.VASP_POSTPRC = user_config.DRIVER_DIR + "/src/vasp2xyzf.py"

    if not hasattr(user_config, 'VASP_NODES'):

        # Number of processors per node to use for a VASP calculation

        if ((user_config.BULK_QM_METHOD == "VASP") or (user_config.IGAS_QM_METHOD == "VASP")):
            print("WARNING: Option config.VASP_NODES was not set")
            print("         Will use a value of 6")

        user_config.VASP_NODES = [6] * user_config.NO_CASES
    else:
        if isinstance(user_config.VASP_NODES, int):
            user_config.VASP_NODES = [user_config.VASP_NODES] * user_config.NO_CASES
        elif isinstance(user_config.VASP_NODES, list):
            if len(user_config.VASP_NODES) > user_config.NO_CASES:
                print("WARNING: Option config.VASP_NODES was set to a list longer than the number of cases")
                print("         Will use the first " + str(user_config.NO_CASES) + " values")
                user_config.VASP_NODES = user_config.VASP_NODES[:user_config.NO_CASES]
            elif len(user_config.VASP_NODES) < user_config.NO_CASES:
                print("WARNING: Option config.VASP_NODES was set to a list shorter than the number of cases")
                print("         Will repeat the last value to fill the list")
                user_config.VASP_NODES = user_config.VASP_NODES + [user_config.VASP_NODES[-1]] * (user_config.NO_CASES - len(user_config.VASP_NODES))
        else:
            print("ERROR: Option config.VASP_NODES was set to an invalid type")
            print("         Acceptable settings are of the form: [int] or int")
            exit()


    if not hasattr(user_config,'VASP_PPN'):

        # Number of nodes to use for a VASP calculation

        if ((user_config.BULK_QM_METHOD == "VASP") or (user_config.IGAS_QM_METHOD == "VASP")):
            print("WARNING: Option config.VASP_PPN was not set")
            print("         Will use a value of config.HPC_PPN")

        user_config.VASP_PPN = user_config.HPC_PPN    
        
    if not hasattr(user_config,'VASP_MEM'):

        # Memory per node to use for a VASP calculation

        if ((user_config.BULK_QM_METHOD == "VASP") or (user_config.IGAS_QM_METHOD == "VASP")):
            print("WARNING: Option config.VASP_MEM was not set")
            #print("         Will use a value of 128 (GB)")

        user_config.VASP_MEM = ""                                   

    if not hasattr(user_config,'VASP_TIME'):

        # Time for a VASP calculation (hrs)

        if ((user_config.BULK_QM_METHOD == "VASP") or (user_config.IGAS_QM_METHOD == "VASP")):
            print("WARNING: Option config.VASP_TIME was not set")
            print("         Will use a value of \"04:00:00\"")

        user_config.VASP_TIME = "04:00:00"
        
    if not hasattr(user_config,'VASP_QUEUE'):

        # Queue for a VASP calculation

        if ((user_config.BULK_QM_METHOD == "VASP") or (user_config.IGAS_QM_METHOD == "VASP")):
            print("WARNING: Option config.VASP_QUEUE was not set")
            print("         Will use pbatch")

        user_config.VASP_QUEUE = "pbatch"
        
    if not hasattr(user_config,'VASP_MODULES'):

        # Queue for a VASP calculation

        if ((user_config.BULK_QM_METHOD == "VASP") or (user_config.IGAS_QM_METHOD == "VASP")):
            print("WARNING: Option config.VASP_MODULES was not set")
            print("         Will use mkl")

        user_config.VASP_MODULES = "mkl"        
        
    if not hasattr(user_config,'VASP_EXE'):

        # VASP executable
        
        if ((user_config.BULK_QM_METHOD == "VASP") or (user_config.IGAS_QM_METHOD == "VASP")):
            print("ERROR: Option config.VASP_EXE was not set")
            print("         Acceptable settings are of the form: \"/path/to/vasp.exe\"")
            exit()
        else:
            user_config.VASP_EXE = None


def check_DFTB(user_config):
    
    """
    
    Checks whether settings for DFTB compatibility.
    Produces warnings for un-initialized values if DFTB is requested
        
    Usage: check_DFTB(user_config)
    
    """    
    
    if not hasattr(user_config,'DFTB_FILES'):

        # Location of basic DFTB+ input files (dftb_in.hsd)

        if ((user_config.BULK_QM_METHOD == "DFTB+") or (user_config.IGAS_QM_METHOD == "DFTB+")):
            print("WARNING: Option config.DFTB_FILES was not set")
            print("         Will use config.WORKING_DIR + \"ALL_BASE_FILES/QM_BASEFILES\"")

        user_config.DFTB_FILES = user_config.WORKING_DIR + "ALL_BASE_FILES/QM_BASEFILES"
    
    if not hasattr(user_config,'DFTB_POSTPRC'):

        # Location of a dftb+ post-processing file ... this should really be in a process_dftb.py file...

        if ((user_config.BULK_QM_METHOD == "DFTB+") or (user_config.IGAS_QM_METHOD == "DFTB+")):
            print("WARNING: Option config.DFTB_POSTPRC was not set")
            print("         Will use config.CHIMES_SRCDIR + \"../contrib/dftbgen_to_xyz.py\"")

        user_config.DFTB_POSTPRC = user_config.CHIMES_SRCDIR + "/../contrib/dftbgen_to_xyz.py"            
    
    if not hasattr(user_config,'DFTB_NODES'):

        # Number of nodes to use for a DFTB calculation

        if ((user_config.BULK_QM_METHOD == "DFTB+") or (user_config.IGAS_QM_METHOD == "DFTB+")):
            print("WARNING: Option config.DFTB_NODES was not set")
            print("         Will use a value of 1")

        user_config.DFTB_NODES = 1
    
    if not hasattr(user_config,'DFTB_PPN'):

        # Number of nodes to use for a DFTB calculation
        
        if ((user_config.BULK_QM_METHOD == "DFTB+") or (user_config.IGAS_QM_METHOD == "DFTB+")):
            print("WARNING: Option config.DFTB_PPN was not set")
            print("         Will use a value of 1")

        user_config.DFTB_PPN = 1 
        
    if not hasattr(user_config,'DFTB_MEM'):

        # Memory per node to to use for a DFTB calculation

        if ((user_config.BULK_QM_METHOD == "DFTB") or (user_config.IGAS_QM_METHOD == "DFTB")):
            print("WARNING: Option config.DFTB_MEM was not set")
            #print("         Will use a value of 128 (GB)")

        user_config.DFTB_MEM = ""                                       

    if not hasattr(user_config,'DFTB_TIME'):

        # Time for a DFTB calculation (hrs)

        if ((user_config.BULK_QM_METHOD == "DFTB+") or (user_config.IGAS_QM_METHOD == "DFTB+")):
            print("WARNING: Option config.DFTB_TIME was not set")
            print("         Will use a value of \"04:00:00\"")

        user_config.DFTB_TIME = "04:00:00"
    
    if not hasattr(user_config,'DFTB_QUEUE'):

        # Queue for a DFTB calculation
        
        if ((user_config.BULK_QM_METHOD == "DFTB+") or (user_config.IGAS_QM_METHOD == "DFTB+")):
            print("WARNING: Option config.DFTB_QUEUE was not set")
            print("         Will use pbatch")

        user_config.DFTB_QUEUE = "pbatch"
    
    if not hasattr(user_config,'DFTB_MODULES'):

        # Queue for a DFTB calculation

        if ((user_config.BULK_QM_METHOD == "DFTB+") or (user_config.IGAS_QM_METHOD == "DFTB+")):
            print("WARNING: Option config.DFTB_MODULES was not set")
            print("         Will use mkl")

        user_config.DFTB_MODULES = "mkl"        
    
    if not hasattr(user_config,'DFTB_EXE'):

        # DFTB+ executable
        
        if ((user_config.BULK_QM_METHOD == "DFTB+") or (user_config.IGAS_QM_METHOD == "DFTB+")):
            print("ERROR: Option config.DFTB_EXE was not set")
            print("         Acceptable settings are of the form: \"/path/to/dftbplus.exe\"")
        
        else:
            user_config.DFTB_EXE = None


def check_CP2K(user_config):
    
    """
    
    Checks whether settings for CP2K compatibility.
    Produces warnings for un-initialized values if CP2K is requested
        
    Usage: check_CP2K(user_config)
    
    """    
    
    if not hasattr(user_config,'CP2K_FILES'):

        # Location of basic CP2K input files (inp and potentials)

        if ((user_config.BULK_QM_METHOD == "CP2K") or (user_config.IGAS_QM_METHOD == "CP2K")):
            print("WARNING: Option config.CP2K_FILES was not set")
            print("         Will use config.WORKING_DIR + \"ALL_BASE_FILES/QM_BASEFILES\"")

        user_config.CP2K_FILES = user_config.WORKING_DIR + "ALL_BASE_FILES/QM_BASEFILES"
    
    if not hasattr(user_config,'CP2K_POSTPRC'):

        # Location of a CP2K post-processing file

        if ((user_config.BULK_QM_METHOD == "CP2K") or (user_config.IGAS_QM_METHOD == "CP2K")):
            print("WARNING: Option config.CP2K_POSTPRC was not set")
            print("         Will use config.DRIVER_DIR + \"/src/cp2k_to_xyz.py\"")

        user_config.CP2K_POSTPRC = user_config.DRIVER_DIR + "/src/cp2k_to_xyz.py"            
    
    if not hasattr(user_config, 'CP2K_NODES'):
        # Number of nodes to use for a CP2K calculation
        if ((user_config.BULK_QM_METHOD == "CP2K") or (user_config.IGAS_QM_METHOD == "CP2K")):
            print("WARNING: Option config.CP2K_NODES was not set")
            print("         Will use a value of 3")
        user_config.CP2K_NODES = [3] * user_config.NO_CASES
    else:
        if isinstance(user_config.CP2K_NODES, int):
            user_config.CP2K_NODES = [user_config.CP2K_NODES] * user_config.NO_CASES
        elif isinstance(user_config.CP2K_NODES, list):
            if len(user_config.CP2K_NODES) > user_config.NO_CASES:
                print("WARNING: Option config.CP2K_NODES was set to a list longer than the number of cases")
                print("         Will use the first " + str(user_config.NO_CASES) + " values")
                user_config.CP2K_NODES = user_config.CP2K_NODES[:user_config.NO_CASES]
            elif len(user_config.CP2K_NODES) < user_config.NO_CASES:
                print("WARNING: Option config.CP2K_NODES was set to a list shorter than the number of cases")
                print("         Will repeat the last value to fill the list")
                user_config.CP2K_NODES = user_config.CP2K_NODES + [user_config.CP2K_NODES[-1]] * (user_config.NO_CASES - len(user_config.CP2K_NODES))
        else:
            print("ERROR: Option config.CP2K_NODES was set to an invalid type")
            print("         Acceptable settings are of the form: [int] or int")
            exit()
    
    if not hasattr(user_config,'CP2K_PPN'):

        # Number of processors per node to use for a CP2K calculation
        
        if ((user_config.BULK_QM_METHOD == "CP2K") or (user_config.IGAS_QM_METHOD == "CP2K")):
            print("WARNING: Option config.CP2K_PPN was not set")
            print("         Will use a value of 1")

        user_config.CP2K_PPN = 1      
        
    if not hasattr(user_config,'CP2K_MEM'):

        # Memory per node to use for a CP2K calculation

        if ((user_config.BULK_QM_METHOD == "CP2K") or (user_config.IGAS_QM_METHOD == "CP2K")):
            print("WARNING: Option config.CP2K_MEM was not set")
            #print("         Will use a value of 128 (GB)")

        user_config.CP2K_MEM = ""                                  

    if not hasattr(user_config,'CP2K_TIME'):

        # Time for a CP2K calculation (hrs)

        if ((user_config.BULK_QM_METHOD == "CP2K") or (user_config.IGAS_QM_METHOD == "CP2K")):
            print("WARNING: Option config.CP2K_TIME was not set")
            print("         Will use a value of \"04:00:00\"")

        user_config.CP2K_TIME = "04:00:00"
    
    if not hasattr(user_config,'CP2K_QUEUE'):

        # Queue for a CP2K calculation
        
        if ((user_config.BULK_QM_METHOD == "CP2K") or (user_config.IGAS_QM_METHOD == "CP2K")):
            print("WARNING: Option config.CP2K_QUEUE was not set")
            print("         Will use pbatch")

        user_config.CP2K_QUEUE = "pbatch"
    
    if not hasattr(user_config,'CP2K_MODULES'):

        # Queue for a CP2K calculation

        if ((user_config.BULK_QM_METHOD == "CP2K") or (user_config.IGAS_QM_METHOD == "CP2K")):
            print("WARNING: Option config.CP2K_MODULES was not set")
            print("         Will use mkl")

        user_config.CP2K_MODULES = "mkl"        
    
    if not hasattr(user_config,'CP2K_EXE'):

        # CP2K executable
        
        if ((user_config.BULK_QM_METHOD == "CP2K") or (user_config.IGAS_QM_METHOD == "CP2K")):
            print("ERROR: Option config.CP2K_EXE was not set")
            print("         Acceptable settings are of the form: \"/path/to/cp2k.popt\"")
            
        else:
            user_config.CP2K_EXE = None    
    
    

def check_GAUS(user_config):
    
    """
    
    Checks whether settings for Gaussian compatibility.
    Produces warnings for un-initialized values if Gaussian is requested
        
    Usage: check_GAUS(user_config)
    
    """

    if not hasattr(user_config,'GAUS_NODES'):

        # Number of nodes to use for a Gaussian calculation

        if user_config.IGAS_QM_METHOD == "Gaussian":
            print("WARNING: Option config.GAUS_NODES was not set")
            print("         Will use a value of 4")

        user_config.GAUS_NODES = 4
        
    if not hasattr(user_config,'GAUS_PPN'):

        # Number of procs per node to use for a Gaussian calculation

        if user_config.IGAS_QM_METHOD == "Gaussian":
            print("WARNING: Option config.GAUS_PPN was not set")
            print("         Will use a value of config.HPC_PPN")

        user_config.GAUS_PPN = user_config.HPC_PPN  
        
    if not hasattr(user_config,'GAUS_MEM'):

        ## Memory per node to use for a GAUS calculation

        if ((user_config.BULK_QM_METHOD == "GAUS") or (user_config.IGAS_QM_METHOD == "GAUS")):
            print("WARNING: Option config.GAUS_MEM was not set")
            #print("         Will use a value of 128 (GB)")

        user_config.GAUS_MEM = ""                                

    if not hasattr(user_config,'GAUS_TIME'):

        # Time for a Gaussian calculation (hrs)

        if user_config.IGAS_QM_METHOD == "Gaussian":
            print("WARNING: Option config.GAUS_TIME was not set")
            print("         Will use a value of \"04:00:00\"")

        user_config.GAUS_TIME = "04:00:00"
        
    if not hasattr(user_config,'GAUS_QUEUE'):

        # Queue for a Gaussian calculation

        if user_config.IGAS_QM_METHOD == "Gaussian":
            print("WARNING: Option config.GAUS_QUEUE was not set")
            print("         Will use pbatch")

        user_config.GAUS_QUEUE = "pbatch"
        
    if not hasattr(user_config,'GAUS_EXE'):

        # Gaussian executable

        if user_config.IGAS_QM_METHOD == "Gaussian":    
            print("ERROR: Option config.GAUS_EXE was not set")
            print("         Acceptable settings are of the form: \"/path/to/gaussian.exe\"")
            exit()            
        else:
            user_config.GAUS_EXE = None
        
    if not hasattr(user_config,'GAUS_SCR'):

        # Gaussian scratch space

        if user_config.IGAS_QM_METHOD == "Gaussian":    
            print("ERROR: Option config.GAUS_SCR was not set")
            print("         Acceptable settings are of the form: \"/path/to/gaussian/scratch/space\"")
            
            exit()            
        else:
            user_config.GAUS_SCR = None
            
    if not hasattr(user_config,'GAUS_REF'):
    
        # Gaussian single atom reference energy file
        
        if user_config.IGAS_QM_METHOD == "Gaussian":
            print("ERROR: Option config.GAUS_REF was not set")
            print("       Provide path to/name of file containing list of")
            print("       <chemical symbol> <Gaussian energy> <planewave code energy>")
            print("       Energies are expected in kcal/mol, and there should be an entry ")
            print("       for each atom type of interest.")
            
            exit()
        else:
            user_config.GAUS_REF = None

def check_LMP(user_config):
    
    """
    
    Checks whether settings for LAMMPS compatibility.
    Produces warnings for un-initialized values if LMP is requested
        
    Usage: check_LMP(user_config)
    
    """    
    
    if not hasattr(user_config,'LMP_FILES'):

        # Location of basic LAMMPS+ input files (data.header.in, data.footer.in, in.lammps)

        if ((user_config.BULK_QM_METHOD == "LMP") or (user_config.IGAS_QM_METHOD == "LMP")):
        
            if hasattr(user_config,'QM_FILES'):
            
                user_config.LMP_FILES = user_config.QM_FILES
            else:
        
                print("WARNING: Option config.LMP_FILES was not set")
                print("         Will use config.WORKING_DIR + \"ALL_BASE_FILES/QM_BASEFILES\"")

                user_config.LMP_FILES = user_config.WORKING_DIR + "ALL_BASE_FILES/QM_BASEFILES"

    if not hasattr(user_config,'LMP_UNITS'):

        # Units LAMMPS will run with - REAL or METAL)

        if ((user_config.BULK_QM_METHOD == "LMP") or (user_config.IGAS_QM_METHOD == "LMP")):
            print("WARNING: Option config.LMP_UNITS was not set")
            print("         Will use \"REAL\"")

        user_config.LMP_UNITS = "REAL"
    
    if not hasattr(user_config,'LMP_POSTPRC'):

        # Location of a LMP post-processing file

        if ((user_config.BULK_QM_METHOD == "LMP") or (user_config.IGAS_QM_METHOD == "LMP")):
            print("WARNING: Option config.LMP_POSTPRC was not set")
            print("         Will use config.DRIVER_DIR + \"/src/lmp_to_xyz.py\"")

        user_config.LMP_POSTPRC = user_config.DRIVER_DIR + "/src/lmp_to_xyz.py"            
    
    if not hasattr(user_config,'LMP_NODES'):

        # Number of nodes to use for a LMP calculation

        if ((user_config.BULK_QM_METHOD == "LMP") or (user_config.IGAS_QM_METHOD == "LMP")):
            print("WARNING: Option config.LMP_NODES was not set")
            print("         Will use a value of 1")

        user_config.LMP_NODES = 1
    
    if not hasattr(user_config,'LMP_PPN'):

        # Number of nodes to use for a LMP calculation
        
        if ((user_config.BULK_QM_METHOD == "LMP") or (user_config.IGAS_QM_METHOD == "LMP")):
            print("WARNING: Option config.LMP_PPN was not set")
            print("         Will use a value of 1")

        user_config.LMP_PPN = 1      
        
    if not hasattr(user_config,'LMP_MEM'):

        # Memory per node to use for a LMP calculation

        if ((user_config.BULK_QM_METHOD == "LMP") or (user_config.IGAS_QM_METHOD == "LMP")):
            print("WARNING: Option config.LMP_MEM was not set")
            #print("         Will use a value of 128 (GB)")

        user_config.LMP_MEM = ""                                  

    if not hasattr(user_config,'LMP_TIME'):

        # Time for a LMP calculation (hrs)

        if ((user_config.BULK_QM_METHOD == "LMP") or (user_config.IGAS_QM_METHOD == "LMP")):
            print("WARNING: Option config.LMP_TIME was not set")
            print("         Will use a value of \"00:30:00\"")

        user_config.LMP_TIME = "00:30:00"
    
    if not hasattr(user_config,'LMP_QUEUE'):

        # Queue for a LMP calculation
        
        if ((user_config.BULK_QM_METHOD == "LMP") or (user_config.IGAS_QM_METHOD == "LMP")):
            print("WARNING: Option config.LMP_QUEUE was not set")
            print("         Will use pdebug")

        user_config.LMP_QUEUE = "pdebug"
    
    if not hasattr(user_config,'LMP_MODULES'):

        # Queue for a LMP calculation

        if ((user_config.BULK_QM_METHOD == "LMP") or (user_config.IGAS_QM_METHOD == "LMP")):
            print("WARNING: Option config.LMP_MODULES was not set")
            print("         Will not load any default modules")

        user_config.LMP_MODULES = None        
    
    if not hasattr(user_config,'LMP_EXE'):

        # LMP executable
        
        if ((user_config.BULK_QM_METHOD == "LMP") or (user_config.IGAS_QM_METHOD == "LMP")):
            print("ERROR: Option config.LMP_EXE was not set")
            print("         Acceptable settings are of the form: \"/path/to/lmp\"")
            
        else:
            user_config.LMP_EXE = None    
    
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

        print("WARNING: Option config.EMAIL_ADD was not set")
        print("         Will not send e-mail updates. ") 
        
        user_config.EMAIL_ADD = False
        

    if not hasattr(user_config,'SEED'):

        # A seed for random selections

        print("WARNING: Option config.SEED was not set")
        print("         Will use a value of 1")    
        
        user_config.SEED          = 1
        

    if not hasattr(user_config,'ATOM_TYPES'):

        # The number of atom types to consider

        print("ERROR: Option config.ATOM_TYPES was not set")
        print("       Acceptable settings are of the form: [\"C\", \"N\" ,\"O\"]")    
        
        exit()
        
    if not hasattr(user_config,'NO_CASES'):

        # The number of cases (state points) to consider

        print("ERROR: Option config.NO_CASES was not set")
        print("       Acceptable settings are of the form of an integer    ")
        
        exit()    
    else:    
        user_config.NO_CASES = int(user_config.NO_CASES)
        

    if not hasattr(user_config,'MOLANAL_SPECIES'):

        # Species to track/plot from molanal... only used for post-processing
        # MOLANAL_SPECIES
        #MOLANAL_SPECIES = ["C1 O1 1(O-C)",
            #               "C1 O2 2(O-C)",
            #               "N2 1(N-N)",
            #               "N1 O1 1(O-N)",
            #               "N2 O1 1(N-N) 1(O-N)",
            #               "O2 1(O-O)"]#

        print("WARNING: Option config.MOLANAL_SPECIES was not set")
        print("         Will use:")
        print("\t",user_config.MOLANAL_SPECIES)
        
        user_config.MOLANAL_SPECIES = user_config.MOLANAL_SPECIES

    if not hasattr(user_config,'USE_AL_STRS'):

           # All cycles after and including USE_AL_STRS will include stress tensors for full self-consisitently obtained frames 
           # Note that for ALC 0, whether stress tensors are included is determined by the settings in config.ALC0_FILES/fm_setup.in 
           # If no stress tensors are desired, set to False (case sensitive)

        print("WARNING: Option config.USE_AL_STRS was not set")
        print("         Will use a value of -1")
        
        user_config.USE_AL_STRS = -1
    else:

        if user_config.USE_AL_STRS < 0:

             user_config.USE_AL_STRS = 1000

    if not hasattr(user_config,'STRS_STYLE'):

        # This controls how stress tensors are included. DIAG means only the 3 diagonal components will be taken. 
        # "ALL" means all 6 unique components are taken.

        print("WARNING: Option config.STRS_STYLE was not set")
        print("         Will use \"ALL\" (i.e. rather than \"DIAG\")")

        user_config.STRS_STYLE    = "ALL"

    if not hasattr(user_config,'THIS_SMEAR'):

        # This parmeter controls which INCAR file is grabbed for VASP calculations. Jobs will use <SMEARING TEMP>.INCAR. If no value is specified, 
        # will use the temperature from the correspoding case in the traj_list file. Assumes case and traj_list.dat ordering match!
        
        print("WARNING: Option config.THIS_SMEAR was not set")
        print("         Will assume values are provided in the traj_list file, in K")

        user_config.THIS_SMEAR = None       # See comment above
        

    if not hasattr(user_config,'DRIVER_DIR'):

        # This driver's src location
        
        print("ERROR: Option config.DRIVER_DIR was not set")
        print("       Acceptable settings are of the form of an absolute path (Unix)")
        
        exit()
        
    if not hasattr(user_config,'WORKING_DIR'):

        # Directory from which all ALCs will be run
        
        print("ERROR: Option config.WORKING_DIR was not set")
        print("       Acceptable settings are of the form of an absolute path (Unix)")
        
        exit()    
        
    if not hasattr(user_config,'CHIMES_SRCDIR'):

        # Location of ChIMES src files ... expects also post_proc_lsq2.py there
        
        print("ERROR: Option config.CHIMES_SRCDIR was not set")
        print("       Acceptable settings are of the form of an absolute path (Unix)")
        
        exit()

    if not hasattr(user_config,'DO_HIERARCH'):

        # Determines whether to build on existing parameter files
        
        print("Warning: Option config.DO_HIERARCH was not set")
        print("         Will use \"False\"")
        
        user_config.DO_HIERARCH = False
        user_config.HIERARCH_PARAM_FILES = []
        user_config.HIERARCH_EXE = None
        user_config.HIERARCH_METHOD = None
    
    if user_config.DO_HIERARCH:
        
        if not hasattr(user_config,'HIERARCH_PARAM_FILES'):

            # Determines whether to build on existing parameter files
            
            print("ERROR: Option config.DO_HIERARCH was set to \"True\", but")
            print("config.HIERARCH_PARAM_FILES not specified")
            
            exit()

        else:
            for i in range(len(user_config.HIERARCH_PARAM_FILES)):
                user_config.HIERARCH_PARAM_FILES[i] = user_config.WORKING_DIR + "ALL_BASE_FILES/HIERARCH_PARAMS/" + user_config.HIERARCH_PARAM_FILES[i]
                
            print("WARNING: config.HIERARCH_PARAM_FILES special cutoffs must") 
            print("         be specified with \"SPECIFIC\" and not \"ALL\"")
            
        if not hasattr(user_config,'HIERARCH_METHOD'):

            # Determines which MD method is used for HIERARCH interaction remoal
            
            print("WARNING: config.HIERARCH_METHOD was not set") 
            print("         Will use config.MD_STYLE")            
            
            user_config.HIERARCH_METHOD = None 

        if not hasattr(user_config,'HIERARCH_EXE'):

            # Determines whether to build on existing parameter files
            
            if user_config.DO_HIERARCH:
            
                print("Warning: Option config.DO_HIERARCH was set to \"True\", but")
                print("         config.HIERARCH_EXE not specified. Will attempt to use MD_MPI or MD_SER")
            
                user_config.HIERARCH_EXE = None                


    ################################
    ##### General HPC options
    ################################

    if not hasattr(user_config,'HPC_PPN'):

        # Number of procs per node

        print("WARNING: Option config.HPC_PPN was not set")
        print("         Will use a value of 36")    
        
        user_config.HPC_PPN = 36
        
    if not hasattr(user_config,'HPC_ACCOUNT'):

        # HPC Charge bank/account

        print("WARNING: Option config.HPC_ACCOUNT was not set")
        print("         Will use pbronze")    
        
        user_config.HPC_ACCOUNT = "pbronze"    
        
    if not hasattr(user_config,'HPC_SYSTEM'):

        # HPC System (i.e. SLURM, Torque, etc.)

        print("WARNING: Option config.HPC_SYSTEM was not set")
        print("         Will use slurm")
        #print("         Note: No other options are currently supported.")    
        
        user_config.HPC_SYSTEM = "slurm"    

        
    if not hasattr(user_config,'HPC_PYTHON'):

        # Path to python executable

        print("WARNING: Option config.HPC_PYTHON was not set")
        print("         Will use python3")
        print("         Note: This script currently requires python3")    
        
        user_config.HPC_PYTHON = "python3"    
        
    if not hasattr(user_config, 'HPC_EMAIL'):

        # Boolean: Have the HPC system send job status emails?

        print("WARNING: Option config.HPC_EMAIL was not set")
        print("         Will use False")
        
        user_config.HPC_EMAIL = False



    ################################
    ##### Correction fitting options
    ################################

    if not hasattr(user_config,'FIT_CORRECTION'):

        # Determines whether to build on existing parameter files
        
        print("Warning: Option config.FIT_CORRECTION was not set")
        print("         Will use \"False\"")
        
        user_config.FIT_CORRECTION          = False
        user_config.CORRECTED_TYPE          = None 
        user_config.CORRECTED_TYPE_FILES    = None
        user_config.CORRECTED_TYPE_EXE      = None 
        user_config.CORRECTED_TEMPS_BY_FILE = None 
        
    if user_config.FIT_CORRECTION:
        
        if not hasattr(user_config,'CORRECTED_TYPE'):

            # Determines whether to build on existing parameter files
            
            if user_config.FIT_CORRECTION:
            
                print("ERROR: Option config.FIT_CORRECTION was set to \"True\", but")
                print("config.CORRECTED_TYPE not specified")
            
                exit()    
            else:
            
                print("Warning: Option config.CORRECTED_TYPE was not set")
                print("         Will use None")        
                user_config.CORRECTED_TYPE = None                
            
        if not hasattr(user_config,'CORRECTED_TYPE_FILES'):

            # Determines whether to build on existing parameter files
            
            if user_config.FIT_CORRECTION:
            
                print("ERROR: Option config.FIT_CORRECTION was set to \"True\", but")
                print("config.CORRECTED_TYPE_FILES not specified")
            
                exit()
            else:
                print("Warning: Option config.CORRECTED_TYPE_FILES was not set")
                print("         Will use None")        
                user_config.CORRECTED_TYPE_FILES = None                
                
        if not hasattr(user_config,'CORRECTED_TYPE_EXE'):

            # Determines whether to build on existing parameter files
            
            if user_config.FIT_CORRECTION:
            
                print("ERROR: Option config.FIT_CORRECTION was set to \"True\", but")
                print("config.CORRECTED_TYPE_EXE not specified")
            
                exit()    
            else:
                print("Warning: Option config.CORRECTED_TYPE_EXE was not set")
                print("         Will use None")        
                user_config.CORRECTED_TYPE_EXE = None            
            
        
        if not hasattr(user_config,'CORRECTED_TEMPS_BY_FILE'):

            # Determines whether to build on existing parameter files
            
            if user_config.FIT_CORRECTION and (user_config.CORRECTED_TYPE == "DFTB"):
            
                print("WARNING: No explicit electron temperature file listed for correction generation.")
                print("         Will attempt to use values in traj_list.dat")
            
                exit()
            else:
                print("Warning: Option config.CORRECTED_TEMPS_BY_FILE was not set")
                print("         Will use None")        
                user_config.CORRECTED_TEMPS_BY_FILE = None            
            
        elif hasattr(user_config,'CORRECTED_TYPE_EXE') and (user_config.CORRECTED_TYPE == "DFTB"):
        
            if user_config.CORRECTED_TEMPS_BY_FILE:
                print("Will attempt to use electron temperatures specified in CORRECTED_TYPE_FILES")
            else:
                print("Will use electron temperatures specified in traj_list.dat")
 

    ################################
    ##### ChIMES LSQ
    ################################
    
    if not hasattr(user_config,'ALC0_FILES'):

        # Location of ALC-0 base files

        print("WARNING: Option config.ALC0_FILES was not set")
        print("         Will use config.WORKING_DIR + \"ALL_BASE_FILES/ALC-0_BASEFILES/\"")
        
        user_config.ALC0_FILES = user_config.WORKING_DIR + "ALL_BASE_FILES/ALC-0_BASEFILES/"

    if not hasattr(user_config,'CHIMES_LSQ'):

        # Location of chimes_lsq executable

        print("WARNING: Option config.CHIMES_LSQ was not set")
        print("         Will use config.CHIMES_SRCDIR + \"chimes_lsq\"")
        
        user_config.CHIMES_LSQ    = user_config.CHIMES_SRCDIR + "chimes_lsq"
        
    if not hasattr(user_config,'CHIMES_LSQ_MODULES'):
    
        print("WARNING: Option config.CHIMES_LSQ_MODULES was not set")
        user_config.CHIMES_LSQ_MODULES = ""

    if not hasattr(user_config,'CHIMES_MD_MODULES'):
    
        print("WARNING: Option config.CHIMES_MD_MODULES was not set")
        user_config.CHIMES_MD_MODULES = ""
  

    if not hasattr(user_config,'CHIMES_SOLVER'):

        # Location of lsq2.py script

        print("WARNING: Option config.CHIMES_SOLVER was not set")
        print("         Will use config.CHIMES_SRCDIR + \"lsq2.py\"")
        
        user_config.CHIMES_SOLVER = user_config.CHIMES_SRCDIR + "lsq2.py"
        
    if not hasattr(user_config,'CHIMES_POSTPRC'):

        # Location of post_proc_lsq2.py script

        print("WARNING: Option config.CHIMES_POSTPRC was not set")
        print("         Will use config.CHIMES_SRCDIR + \"/../build/post_proc_chimes_lsq.py\"")
        
        user_config.CHIMES_POSTPRC = user_config.CHIMES_SRCDIR + "/../build/post_proc_chimes_lsq.py"


    if not hasattr(user_config,'N_HYPER_SETS'):

        # Number of unique fm_setup.in files; allows fitting, e.g., multiple overlapping models to the same data 

        print("WARNING: Option config.N_HYPER_SETS was not set")
        print("         Will set to a value of 1 (old mode)")

        user_config.N_HYPER_SETS = 1

    if not hasattr(user_config,'WEIGHTS_SET_ALC_0'):

        # Should a file of user-specified weights be used to set ALC-0
        # (or ALC-1, if no clustering) weights?

        print("WARNING: Option config.WEIGHTS_SET_ALC_0 was not set")
        print("         Will set to False")
        
        user_config.WEIGHTS_SET_ALC_0 = False    

    if not hasattr(user_config,'WEIGHTS_ALC_0'):

        # File of user-specified weights - only used if WEIGHTS_SET_ALC_0 true

        print("WARNING: Option config.WEIGHTS_ALC_0 was not set")
        print("         Will set to None")
        
        user_config.WEIGHTS_ALC_0 = None    
    
    if not hasattr(user_config,'WEIGHTS_FORCE'):

        # Weights for bulk frame forces

        print("WARNING: Option config.WEIGHTS_FORCE was not set")
        print("         Will use a value of 1.0")
        
        user_config.WEIGHTS_FORCE = [ ["A"],[[1.0]]]
    elif isinstance(user_config.WEIGHTS_FORCE,float):
            user_config.WEIGHTS_FORCE = [ ["A"],[[user_config.WEIGHTS_FORCE]]]
        
    if not hasattr(user_config,'WEIGHTS_FGAS'):

        # Weights for gas frame forces
        
        # Notes on WEIGHTS_FGAS: If positive, a single weight value is used. Otherwise, values are automatically set to
        # -WEIGHTS_FGAS/<natoms in cluster>, where W_FGAS is should be max atoms in the training traj 

        print("WARNING: Option config.WEIGHTS_FGAS was not set")
        print("         Will use a value of 5.0")
        
        user_config.WEIGHTS_FGAS = [ ["A"],[[5.0]]]
    elif isinstance(user_config.WEIGHTS_FGAS,float):
            user_config.WEIGHTS_FGAS = [ ["A"],[[user_config.WEIGHTS_FGAS]]]
                                

    if not hasattr(user_config,'WEIGHTS_ENER'):

        # Weights for bulk frame energies

        print("WARNING: Option config.WEIGHTS_ENER was not set")
        print("         Will use a value of 0.1")
        
        user_config.WEIGHTS_ENER = [ ["A"],[[0.1]]]
    elif isinstance(user_config.WEIGHTS_ENER,float):
            user_config.WEIGHTS_ENER = [ ["A"],[[user_config.WEIGHTS_ENER]]]
        
    
    if not hasattr(user_config,'WEIGHTS_EGAS'):

        # Weights for gas frame energies

        print("WARNING: Option config.WEIGHTS_EGAS was not set")
        print("         Will use a value of 0.1")
        
        user_config.WEIGHTS_EGAS = [ ["A"],[[0.1]]]
    elif isinstance(user_config.WEIGHTS_EGAS,float):
            user_config.WEIGHTS_EGAS = [ ["A"],[[user_config.WEIGHTS_EGAS]]]
        
    if not hasattr(user_config,'WEIGHTS_STRES'):

        # Weights for stress tensor components

        print("WARNING: Option config.WEIGHTS_STRES was not set")
        print("         Will use a value of 250.0")
        
        user_config.WEIGHTS_STRES = [ ["A"],[[250.0]]]
    elif isinstance(user_config.WEIGHTS_STRES,float):
            user_config.WEIGHTS_STRES = [ ["A"],[[user_config.WEIGHTS_STRES]]]

    if not hasattr(user_config,'REGRESS_ALG'):

        # What regression algorithm should be used?

        print("WARNING: Option config.REGRESS_ALG was not set")
        print("         Will use dlasso")
        
        user_config.REGRESS_ALG = "dlasso"
        
    if not hasattr(user_config,'REGRESS_NRM'):

        # Should the regression algorithm normalize the problem first?

        print("WARNING: Option config.REGRESS_NRM was not set")
        print("         Will use a value of True")
        
        user_config.REGRESS_NRM = True    # Note: Default behavior is true!
        
    if not hasattr(user_config,'REGRESS_VAR'):

        # The regression regularization variable

        print("WARNING: Option config.REGRESS_VAR was not set")
        print("         Will use a value of 1.0E-5")
        
        user_config.REGRESS_VAR = 1.0E-5                

    if not hasattr(user_config,'CHIMES_BUILD_NODES'):

        # The number of nodes to use for chimes_lsq

        print("WARNING: Option config.CHIMES_BUILD_NODES was not set")
        print("         Will use a value of 4")
        
        user_config.CHIMES_BUILD_NODES = 4

    if not hasattr(user_config,'CHIMES_BUILD_QUEUE'):

        # The queue to submit the chimes_lsq job to

        print("WARNING: Option config.CHIMES_BUILD_QUEUE was not set")
        print("         Will use pbatch")
        
        user_config.CHIMES_BUILD_QUEUE = "pbatch"
        
    if not hasattr(user_config,'CHIMES_BUILD_TIME'):

        # How long the job should be submitted for (hours)

        print("WARNING: Option config.CHIMES_BUILD_TIME was not set")
        print("         Will use \"04:00:00\"")
        
        user_config.CHIMES_BUILD_TIME = "04:00:00"        

    if not hasattr(user_config,'CHIMES_SOLVE_NODES'):

        # The number of nodes to use when solving the design matrix

        print("WARNING: Option config.CHIMES_SOLVE_NODES was not set")
        print("         Will use a value of 8")
        
        user_config.CHIMES_SOLVE_NODES = 8
        
    if not hasattr(user_config,'CHIMES_SOLVE_PPN'):

        # The number of procs per nodes to use when solving the design matrix

        print("WARNING: Option config.CHIMES_SOLVE_PPN was not set")
        print("         Will use a value of config.HPC_PPN")
        
        user_config.CHIMES_SOLVE_PPN = user_config.HPC_PPN        

    if not hasattr(user_config,'CHIMES_SOLVE_QUEUE'):

        # The queue to use when solving the design matrix

        print("WARNING: Option config.CHIMES_SOLVE_QUEUE was not set")
        print("         Will use pbatch")
        
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

        print("WARNING: Option config.CHIMES_SOLVE_TIME was not set")
        print("         Will use \"24:00:00\"")
        
        user_config.CHIMES_SOLVE_TIME = "24:00:00"

    ################################
    ##### ChIMES MD
    ################################

    if not hasattr(user_config,'MD_STYLE'):

        # Simulation method, i.e. ChIMES MD or DFTBplus+ChIMES

        print("ERROR: Simulation mode not specified!")
        print("         config.MD_STYLE must be set to \"CHIMES\", \"LMP\", or \"DFTB\"")
        exit()
    else:
        print("Will run simulations using method: ", user_config.MD_STYLE)
    
    
    if hasattr(user_config,'CHIMES_MD'):

        # Path to chimes_md executable

        print("WARNING: Defunct option config.CHIMES_MD was set")
        print("         Ignoring. Will search for config.CHIMES_MD_SER and config.CHIMES_MD_MPI")
        
    if not hasattr(user_config,'CHIMES_MD_SER'):

        # Path to the serial chimes_md executable

        print("WARNING: Option config.CHIMES_MD_SER was not set")
        print("         Will use config.CHIMES_SRCDIR + \"chimes_md-serial\"")
        
        user_config.CHIMES_MD_SER = user_config.CHIMES_SRCDIR + "chimes_md-serial"        
    
    if user_config.MD_STYLE == "CHIMES":
        
        if not hasattr(user_config,'CHIMES_MD_MPI'):

            # Path to chimes_md executable

            print("WARNING: Option config.CHIMES_MD_MPI was not set")
            print("         Will use config.CHIMES_SRCDIR + \"chimes_md-mpi\"")
        
            user_config.CHIMES_MD_MPI = user_config.CHIMES_SRCDIR + "chimes_md-mpi"

    else:
    	if not hasattr(user_config,'MD_MPI'):
            print("ERROR: Option config.MD_MPI was not set")
            exit(0)
            
    	if not hasattr(user_config,'MD_SER'): 
            print("WARNING: Option config.MD_SER was not set")
            print("         Attempting to set equal to config.MD_MPI")
            
            user_config.MD_SER = user_config.MD_MPI
            
    	user_config.CHIMES_MD_MPI = None
    	user_config.CHIMES_MD_SER = None
        
    if not hasattr(user_config,'MOLANAL'):

        # Path to molanal executable

        print("Error: Option config.MOLANAL was not set")
        print("       Acceptable settings are of the form of an absolute path (Unix)")
        
    
        
    if not hasattr(user_config,'MDFILES'):

        # Path to the base chimes_md files (i.e. input.xyz's and run_md.in's)

        print("WARNING: Option config.MDFILES was not set")
        print("         Will use config.WORKING_DIR + \"ALL_BASE_FILES/CHIMESMD_BASEFILES/\"")
        
        user_config.MDFILES = user_config.WORKING_DIR + "ALL_BASE_FILES/CHIMESMD_BASEFILES/"

    if not hasattr(user_config,'CHIMES_PEN_PREFAC'):

        # Penalty function prefactor

        print("WARNING: Option config.CHIMES_PEN_PREFAC was not set")
        print("         Will use a value of 1.0E6")
        
        user_config.CHIMES_PEN_PREFAC = 1.0E6
        
    if not hasattr(user_config,'CHIMES_PEN_DIST'):

        # Penalty function kick-in distance

        print("WARNING: Option config.CHIMES_PEN_DIST was not set")
        print("         Will use a value of 0.02")
        
        user_config.CHIMES_PEN_DIST = 0.02        

    if not hasattr(user_config,'MD_NODES'):

        # Number of nodes to use for MD jobs

        print("WARNING: Option config.MD_NODES was not set")
        print("         Will use a value of 8 for all cases")
        
        user_config.MD_NODES = [4]*user_config.NO_CASES
        
    elif hasattr(user_config,'MD_NODES') and (len(user_config.MD_NODES) != user_config.NO_CASES):
        print("ERROR: Option config.MD_NODES should be provided in the ")
        print("       form of a NO_CASES long list, e.g. [4]*NO_CASES.")
        exit()                
        
    if not hasattr(user_config,'MD_QUEUE'):

        # Queue to use for MD jobs

        print("WARNING: Option config.MD_QUEUE was not set")
        print("         Will use pbatch for all cases")
        
        user_config.MD_QUEUE = ["pbatch"]*user_config.NO_CASES
        
    elif hasattr(user_config,'MD_QUEUE') and (len(user_config.MD_QUEUE) != user_config.NO_CASES):
        print("ERROR: Option config.MD_QUEUE should be provided in the ")
        print("       form of a NO_CASES long list, e.g. [\"pbatch\"]*NO_CASES.")
        exit()        
        
    if not hasattr(user_config,'MD_TIME'):

        # Time to request for MD jobs (hours)

        print("WARNING: Option config.MD_TIME was not set")
        print("         Will use a value of \"4:00:00\" for all cases")
        
        user_config.MD_TIME = ["4:00:00"]*user_config.NO_CASES
        
    elif hasattr(user_config,'MD_TIME') and (len(user_config.MD_TIME) != user_config.NO_CASES):
        print("ERROR: Option config.MD_TIME should be provided in the ")
        print("       form of a NO_CASES long list, e.g. [\"4:00:00\"]*NO_CASES.")
        exit()

    ################################
    ##### Cluster specific paths/variables
    ################################

    if not hasattr(user_config,'DO_CLUSTER'):

        # Should cluster extraction/use be performed?
        # ... I don't think "False" is actually implemented yet... 

        print("WARNING: Option config.DO_CLUSTER was not set")
        print("         Will use a value of False")
        #print "        Note: \"False\" is not current supported"
        
        user_config.DO_CLUSTER = False
        user_config.MAX_CLUATM = None
        user_config.TIGHT_CRIT = None
        user_config.LOOSE_CRIT = None
        user_config.CLU_CODE   = None
        
    if user_config.DO_CLUSTER:

        if not hasattr(user_config,'MAX_CLUATM'):

            # Max number of atoms to consider in a cluster

            print("WARNING: Option config.MAX_CLUATM was not set")
            print("         Will use a value of 100")

            user_config.MAX_CLUATM = 100
                 
        if not hasattr(user_config,'TIGHT_CRIT'):

            # File with tight clustering criteria

            print("WARNING: Option config.TIGHT_CRIT was not set")
            print("         Will use config.WORKING_DIR + \"ALL_BASE_FILES/tight_bond_crit.dat\"")

            user_config.TIGHT_CRIT = user_config.WORKING_DIR + "ALL_BASE_FILES/tight_bond_crit.dat"
            
        if not hasattr(user_config,'LOOSE_CRIT'):

            # File with loose clustering criteria... if set equal to the tight criteria file,
            # then no "loose" (i.e. "ts") clusters are generated.

            print("WARNING: Option config.LOOSE_CRIT was not set")
            print("         Will use config.WORKING_DIR + \"ALL_BASE_FILES/loose_bond_crit.dat\"")

            user_config.LOOSE_CRIT = user_config.WORKING_DIR + "ALL_BASE_FILES/loose_bond_crit.dat"        
            
        if not hasattr(user_config,'CLU_CODE'):

            # Cluster extraction code

            print("WARNING: Option config.CLU_CODE was not set")
            print("         Will use config.DRIVER_DIR  + \"/../utilities/new_ts_clu.cpp\"")

            user_config.CLU_CODE = user_config.DRIVER_DIR  + "/../utilities/new_ts_clu.cpp"
                

        ################################
        ##### ALC-specific variables ... Note: Hardwired for partial memory mode
        ################################

        if not hasattr(user_config,'MEM_BINS'):

            # number of bins for histograms (cluster selection)

            print("WARNING: Option config.MEM_BINS was not set")
            print("         Will use a value of 40")

            user_config.MEM_BINS = 40    
        
        if not hasattr(user_config,'MEM_CYCL'):

            # number of cycles for cluster selection

            print("WARNING: Option config.MEM_CYCL was not set")
            print("         Will use a value of config.MEM_BINS/10")

            user_config.MEM_CYCL = user_config.MEM_BINS/10        
        
        if not hasattr(user_config,'MEM_NSEL'):

            # number of clusters to select each ALC

            print("WARNING: Option config.MEM_NSEL was not set")
            print("         Will use a value of 400")

            user_config.MEM_NSEL = 400
            
        if not hasattr(user_config,'MEM_ECUT'):

            # Energy cutoff (E/atom in kcal/mol) cutoff for cluster selection

            print("WARNING: Option config.MEM_ECUT was not set")
            print("         Will use a value of 100.0")

            user_config.MEM_ECUT = 100.0        
            
        if not hasattr(user_config,'CALC_REPO_ENER_CENT_QUEUE'):

            # Queue for central repo energy calculations

            print("WARNING: Option config.CALC_REPO_ENER_CENT_QUEUE was not set")
            print("         Will use pbatch")

            user_config.CALC_REPO_ENER_CENT_QUEUE = "pdebug"
            
        if not hasattr(user_config,'CALC_REPO_ENER_CENT_TIME'):

            # Time for central repo energy calculations

            print("WARNING: Option config.CALC_REPO_ENER_CENT_TIME was not set")
            print("         Will use a value of \"00:10:00\"")

            user_config.CALC_REPO_ENER_CENT_TIME =  "00:10:00"    
            
        if not hasattr(user_config,'CALC_REPO_ENER_QUEUE'):

            # Queue for central repo energy calculations

            print("WARNING: Option config.CALC_REPO_ENER_QUEUE was not set")
            print("         Will use pbatch")

            user_config.CALC_REPO_ENER_QUEUE = "pbatch"
            
        if not hasattr(user_config,'CALC_REPO_ENER_TIME'):

            # Time for central repo energy calculations

            print("WARNING: Option config.CALC_REPO_ENER_TIME was not set")
            print("         Will use a value of \"04:00:00\"")

            user_config.CALC_REPO_ENER_TIME =  "04:00:00"                
            

    ################################
    ##### QM-Specific variables
    ################################

    if not hasattr(user_config,'BULK_QM_METHOD'):

        # Software/method for calculating Forces/stresses/energies for bulk configurations
        # Currently only VASP is supported, but CP2K should be included in the future

        print("WARNING: Option config.BULK_QM_METHOD was not set")
        print("         Will use VASP")

        user_config.BULK_QM_METHOD = "VASP"
        
    if not hasattr(user_config,'IGAS_QM_METHOD'):

        # Software/method for calculating Forces/stresses/energies for gas configurations
        # Currently, can also use "Gaussian... requires assignment of additional vars, checked below
        #
        # Note that if Gaussian is used, single-atom-energy offsets are hardcoded currentlly (see process_gaussian.py)
        # NWChem should be added in the future

        if user_config.DO_CLUSTER:
            print("WARNING: Option config.IGAS_QM_METHOD was not set")
            print("         Will use VASP")

        user_config.IGAS_QM_METHOD = "VASP"  
        
    if not hasattr(user_config,'QM_FILES'):

        # Location of basic QM input files (INCAR, KPOINTS, etc)
        
        print("WARNING: Option config.QM_FILES was not set")
        print("         Will use config.WORKING_DIR + \"ALL_BASE_FILES/QM_BASEFILES\"")

        user_config.QM_FILES = user_config.WORKING_DIR + "ALL_BASE_FILES/QM_BASEFILES"              

    # If a given reference (QM) method is not used, set defaults silently
    # In this case they are unused, but ensure function call compatibility
    
    if (user_config.IGAS_QM_METHOD == "VASP") or (user_config.BULK_QM_METHOD == "VASP"):
        check_VASP(user_config)
    else:
        user_config.VASP_POSTPRC = None
        user_config.VASP_NODES   = [None] * user_config.NO_CASES  #This needs to be a list since in main.py we enumarate it
        user_config.VASP_PPN     = None 
        user_config.VASP_MEM     = None 
        user_config.VASP_TIME    = None
        user_config.VASP_QUEUE   = None
        user_config.VASP_MODULES = None
        user_config.VASP_EXE     = None
        
    if (user_config.IGAS_QM_METHOD == "DFTB+") or (user_config.BULK_QM_METHOD == "DFTB+"):    
        check_DFTB(user_config)
    else:
        user_config.DFTB_FILES   = None
        user_config.DFTB_POSTPRC = None
        user_config.DFTB_NODES   = None 
        user_config.DFTB_PPN     = None 
        user_config.DFTB_MEM     = None 
        user_config.DFTB_TIME    = None
        user_config.DFTB_QUEUE   = None
        user_config.DFTB_MODULES = None 
        user_config.DFTB_EXE     = None
        
    if (user_config.IGAS_QM_METHOD == "CP2K") or (user_config.BULK_QM_METHOD == "CP2K"):    
        check_CP2K(user_config)
    else:
        user_config.CP2K_FILES   = None
        user_config.CP2K_POSTPRC = None
        user_config.CP2K_NODES   = [None] * user_config.NO_CASES #This needs to be a list since in main.py we enumarate it 
        user_config.CP2K_PPN     = None 
        user_config.CP2K_MEM     = None 
        user_config.CP2K_TIME    = None
        user_config.CP2K_QUEUE   = None
        user_config.CP2K_MODULES = None 
        user_config.CP2K_EXE     = None  
        user_config.CP2K_DATADIR = None      
        
    if (user_config.IGAS_QM_METHOD == "GAUS") or (user_config.BULK_QM_METHOD == "GAUS"):
        check_GAUS(user_config)
    else:
        user_config.GAUS_NODES   = None
        user_config.GAUS_PPN     = None
        user_config.GAUS_MEM     = None
        user_config.GAUS_TIME    = None 
        user_config.GAUS_QUEUE   = None
        user_config.GAUS_EXE     = None
        user_config.GAUS_SCR     = None
        user_config.GAUS_REF     = None

    if (user_config.IGAS_QM_METHOD == "LMP") or (user_config.BULK_QM_METHOD == "LMP"):
        check_LMP(user_config)
    else:
        user_config.LMP_POSTPRC = None
        user_config.LMP_NODES   = None
        user_config.LMP_PPN     = None 
        user_config.LMP_MEM     = None 
        user_config.LMP_TIME    = None
        user_config.LMP_QUEUE   = None
        user_config.LMP_MODULES = None
        user_config.LMP_EXE     = None
        user_config.LMP_UNITS   = None
