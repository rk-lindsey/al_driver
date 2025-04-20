# Global (python) modules

import os
import sys
import glob

# Local modules

import helpers
import gen_ff
import run_md
import cluster
import gen_selections
import qm_driver
import restart
import verify_config
import pretty_stuff

# Allow config file to be read from local directory

local_path = os.path.normpath(helpers.run_bash_cmnd("pwd").rstrip())
sys.path.append(local_path)

import config  # User-specified "global" vars

def main(args):

    """ 
    
    Code Author: Rebecca K Lindsey (RKL) - 2019

    Active Learning Driver Main.

    Usage: unbuffer python ../PYTHON_DRIVER/main.py 0 1 2 | tee driver.log 

    Notes: 

           - If "unbuffer" command is unavailable on your system, try replacing "unuffer python" with "python -u"

           - Run location is specified in the config file (WORKING_DIR), NOT the directory 
             it was launched from
             
           - If "unbuffer" command is unavailable on your system, try replacing "unuffer python" with "python -u"
    
           - This tool works most effectively when run with something like screen, tmux, or nohup 
             during remote runs (these utils allow the session to be detached/reattached)    
    
           - Build documentation with: ./build_docs.sh 
             ...This will create .html files in the doc directory that can be opened
         with any browser (i.e. firefox, if running on the LC)    
    
           - Second argument to main.py is a list of cycles to run (i.e. ALC-0, ALC-, ALC-2)
             ... This must ALWAYS be a sequence starting from 0, even when restarting
    
           - Driver will continue from last completed task in restart.dat, if the file is found     
         
           - If THIS_SMEAR is set in config.py, <THIS_SMEAR>.INCAR will be used for all VASP
             calculations, for all cases. If it is NOT set, <T_Case>.INCAR will be used, where 
         <T_Case> is the last column for rows n+1 in the traj_list.dat file. Note that this 
         assumes case ordering matches file ordering in traj_list.dat.

    WARNING: Assumes lsq2.py is using the ***hardcoded*** DLARS path
    
    WARNING: Ensure all queued jobs have ended or been killed before restarting    

    WARNING: FIRST/FIRSTALL in fm_setup.in file unsupported for ALC > 0. To add stress tensors 
             in later ALC, set USE_AL_STRS and STRS_STYLE in your config.py

    WARNING: AL does not (yet) support different stress/energy options for different cases

    WARNING: This driver does NOT support SPLITFI functionality in fm_setup.in file. A-matrix
             is handled by the driver itself, based on CHIMES_SOLVE_NODES, CHIMES_SOLVE_PPN,
         and CHIMES_SOLVE_QUEUE. Note that number of files is CHIMES_SOLVE_NODES*CHIMES_SOLVE_PPN.
         To allow more memory per task, increase nodes and decrease ppn. Script will still request
         full nodes.

    WARNING: Per-atom energies will be incorrect if number of atoms for multiple types is 
             identical across the entire A-mat (i.e. for a CO system) ... This can be/is
         rectified by running additional AL cycles that extracts individual molecules
         
    To Do: 
               
           - Update/improve vasp2xyzf.py
           
           - Add a test suite        
           
           - Add an ability to go back and run additional independent simulations for various ALC's/cases    
           
           - Add ability to use AL-driver for DFTB model fitting (DFTB+)
           
           - Add ability to subtract off contributions from an external simulation (LAMMPS)
           
           - Add support for LAMMPS as a MD method
           
           - Refactor supported delta-learning methods; give appropriate name
           
           - Refactor supported hierarchical transfer learning; give appropriate name
           
           - Add support for multi-resolution/scale model development (Frankenstein A-matrices/dual parameter files)
        
    """           
        
    ################################
    # Print Pretty Stuff
    ################################

    pretty_stuff.print_pretty_stuff()        

    ################################
    # Initialize vars
    ################################

    THIS_CASE  = 0
    THIS_INDEP = 0
    EMAIL_ADD  = ''
    SMEARING   = "TRAJ_LIST"
    
    if os.path.normpath(config.WORKING_DIR) != local_path:
    
        print("Error: this script was not run from config.WORKING_DIR!")
        print("config.WORKING_DIR:",config.WORKING_DIR)
        print("local path:        ",local_path)
        print("Exiting.")
        
        exit()
        
    ################################
    # Verify contents of config.py
    ################################
        
        
    # Check whether the user just requested help
    
    if "--help" in args:
        verify_config.print_help()
        exit()
    
    verify_config.verify(config)
    
    print("The following has been set as the working directory:")
    print('\t', config.WORKING_DIR)
    print("The ALC-X contents of this directory will be overwritten.")

    ################################
    # Pre-process user specified variables
    ################################

    config.ATOM_TYPES.sort()

    config.CHIMES_SOLVER  = config.HPC_PYTHON + " " + config.CHIMES_SOLVER
    config.CHIMES_POSTPRC = config.HPC_PYTHON + " " + config.CHIMES_POSTPRC
    
    if ((config.BULK_QM_METHOD == "VASP") or (config.IGAS_QM_METHOD == "VASP")):
        config.VASP_POSTPRC   = config.HPC_PYTHON + " " + config.VASP_POSTPRC
    if ((config.BULK_QM_METHOD == "DFTB+") or (config.IGAS_QM_METHOD == "DFTB+")):
        config.DFTB_POSTPRC   = config.HPC_PYTHON + " " + config.DFTB_POSTPRC
    if ((config.BULK_QM_METHOD == "CP2K") or (config.IGAS_QM_METHOD == "CP2K")):
        config.CP2K_POSTPRC   = config.HPC_PYTHON + " " + config.CP2K_POSTPRC     
    if ((config.BULK_QM_METHOD == "LMP") or (config.IGAS_QM_METHOD == "LMP")):
        config.LMP_POSTPRC   = config.HPC_PYTHON + " " + config.LMP_POSTPRC        

    
    if config.EMAIL_ADD:
        EMAIL_ADD = config.EMAIL_ADD    
        
    if config.THIS_SMEAR:
        SMEARING = config.THIS_SMEAR

        print("Will use a smearing temperature of",SMEARING,"K")
    else:
        print("Will read smearing temperatures from traj_list.dat file")    
        

    # Needed for backward compatibility
    
    if hasattr(config, "CHIMES_MD_MPI") and not hasattr(config,"MD_MPI"):
        config.MD_MPI = config.CHIMES_MD_MPI
    
    if hasattr(config, "CHIMES_MD_SER") and not hasattr(config,"MD_SER"):
        config.MD_SER = config.CHIMES_MD_SER 
        
    if hasattr(config, "CHIMES_MD_MODULES") and not hasattr(config,"MD_MODULES"):
        config.MD_MODULES = config.CHIMES_MD_MODULES   
	

    if (config.DO_HIERARCH) and (config.HIERARCH_METHOD is None):
        config.HIERARCH_METHOD = config.MD_STYLE
        print("Set config.HIERARCH_METHOD to", config.MD_STYLE) 

    if (config.DO_HIERARCH) and (config.HIERARCH_EXE is None):
        try:
            config.HIERARCH_EXE = config.MD_SER
            print("Set config.HIERARCH_EXE to", config.MD_SER) 
        except:
            config.HIERARCH_EXE = config.MD_MPI 
            print("Set config.HIERARCH_EXE to", config.MD_MPI)        

    ################################
    ################################
    # Begin Active Learning
    ################################
    ################################

    print("Will run for the following active learning cycles:")

    ALC_LIST = args

    for THIS_ALC in ALC_LIST:
        print(THIS_ALC)
        

    # Set up the restart file
        
    restart_controller = restart.restart() # Reads/creates restart file. Must be named "restart.dat"

    ALC_LIST = restart_controller.update_ALC_list(ALC_LIST)

    print("After processing restart file, will run for the following active learning cycles:")

    for THIS_ALC in ALC_LIST:
        print(THIS_ALC)
        
    if type(config.USE_AL_STRS) is int:
        print("Will include stress tensors for self-consistently obtained full-frames, for ALC >=",config.USE_AL_STRS)
    
    else:
        config.USE_AL_STRS = ALC_LIST[-1]+1 # Set to one greater than the number of requested ALCs


    for THIS_ALC in ALC_LIST:

        THIS_ALC = int(THIS_ALC)
                
        # Let the ALC process know whether this is a restarted cycle or a completely new cycle
        
        if THIS_ALC != restart_controller.last_ALC:
        
            restart_controller.reinit_vars()

        if (THIS_ALC == 0) and     (not config.DO_CLUSTER):
            print("config.DO_CLUSTER was set false - skipping ALC-0")
            continue
        
        
        # Prepare the restart file

        restart_controller.update_file("ALC: " + str(THIS_ALC) + '\n')
            

        print("Working on ALC:", THIS_ALC)

        os.chdir(config.WORKING_DIR)
        

        # Begins in the working directory (WORKING_DIR)

        if THIS_ALC == 0: # Then this is the first ALC, so we need to do things a bit differently ... 
        
        
            if not restart_controller.BUILD_AMAT: # Then we haven't even begun this ALC

                # Set up/move into the ALC directory
            
                helpers.run_bash_cmnd("rm -rf ALC-" + str(THIS_ALC))
                helpers.run_bash_cmnd("mkdir  ALC-" + str(THIS_ALC))
            
            os.chdir("ALC-" + str(THIS_ALC))
            
                    
            ################################
            # Generate the force field    
            ################################
            
            if not restart_controller.BUILD_AMAT:
            
                # Note: Stress tensor inclusion controlled by contents of config.ALC0_FILES
            
                active_job = gen_ff.build_amat(THIS_ALC,
                        do_hierarch        = config.DO_HIERARCH,
			hierarch_method    = config.HIERARCH_METHOD,
                        hierarch_files     = config.HIERARCH_PARAM_FILES,    
                        hierarch_exe       = config.HIERARCH_EXE,
                        do_correction      = config.FIT_CORRECTION,
                        correction_method  = config.CORRECTED_TYPE,
                        correction_files   = config.CORRECTED_TYPE_FILES,
                        correction_exe     = config.CORRECTED_TYPE_EXE,
                        correction_temps   = config.CORRECTED_TEMPS_BY_FILE,                        
                        prev_gen_path      = config.ALC0_FILES,
                        job_email          = config.HPC_EMAIL,
                        job_ppn            = str(config.HPC_PPN),
                        job_nodes          = config.CHIMES_BUILD_NODES,
                        job_walltime       = config.CHIMES_BUILD_TIME,    
                        job_queue          = config.CHIMES_BUILD_QUEUE,        
                        job_account        = config.HPC_ACCOUNT, 
                        job_system         = config.HPC_SYSTEM,
                        job_executable     = config.CHIMES_LSQ)
                        
                helpers.wait_for_job(active_job, job_system = config.HPC_SYSTEM, verbose = True, job_name = "build_amat")

                restart_controller.update_file("BUILD_AMAT: COMPLETE" + '\n')
                
                helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "BUILD_AMAT: COMPLETE ")    
            else:
                restart_controller.update_file("BUILD_AMAT: COMPLETE" + '\n')

            if not restart_controller.SOLVE_AMAT:
            
                if not gen_ff.solve_amat_started(): 
                
                    print("Starting solve_amat from scratch")            
            
                    active_job = gen_ff.solve_amat(THIS_ALC, 
                        weights_set_alc_0  = config.WEIGHTS_SET_ALC_0,
                        weights_alc_0      = config.WEIGHTS_ALC_0,
                        weights_force      = config.WEIGHTS_FORCE,
                        weights_force_gas  = config.WEIGHTS_FGAS,
                        weights_energy     = config.WEIGHTS_ENER,
                        weights_energy_gas = config.WEIGHTS_EGAS,
                        weights_stress     = config.WEIGHTS_STRES,
                        regression_alg     = config.REGRESS_ALG,
                        regression_nrm     = config.REGRESS_NRM,
                        regression_var     = config.REGRESS_VAR,
                        job_email          = config.HPC_EMAIL,
                        job_ppn            = str(config.HPC_PPN),
                        node_ppn           = config.HPC_PPN,
                        job_nodes          = config.CHIMES_SOLVE_NODES,
                        job_walltime       = config.CHIMES_SOLVE_TIME,    
                        job_queue          = config.CHIMES_SOLVE_QUEUE,                    
                        job_account        = config.HPC_ACCOUNT, 
                        job_system         = config.HPC_SYSTEM,
                        job_executable     = config.CHIMES_SOLVER)    
                        
                    helpers.wait_for_job(active_job, job_system = config.HPC_SYSTEM, verbose = True, job_name = "solve_amat")

                
                # Check whether the amat_solve job has completed and keep track of how many times it has run

                n_restarts = 0

                while not gen_ff.solve_amat_completed():

                    n_restarts += 1

                    print("solve amat job incomplete... restarting for the ", n_restarts, "st/nd/th time")
                    
                    active_job = gen_ff.restart_solve_amat(THIS_ALC,
                        regression_alg     = config.REGRESS_ALG,
                        regression_nrm     = config.REGRESS_NRM,
                        regression_var     = config.REGRESS_VAR,    
                        job_email          = config.HPC_EMAIL,        
                        job_ppn            = config.CHIMES_SOLVE_PPN,
                        node_ppn           = config.HPC_PPN,
                        job_nodes          = config.CHIMES_SOLVE_NODES,
                        job_walltime       = config.CHIMES_SOLVE_TIME,    
                        job_queue          = config.CHIMES_SOLVE_QUEUE,    
                        job_account        = config.HPC_ACCOUNT, 
                        job_system         = config.HPC_SYSTEM,
                        job_executable     = config.CHIMES_SOLVER)    
                    
                    helpers.wait_for_job(active_job, job_system = config.HPC_SYSTEM, verbose = True, job_name = "restart_solve_amat")
                    

                #if n_restarts > 0: # Then we need to manually build the parameter file

                if not os.path.isfile("GEN_FF/params.txt"):
                    print("ERROR: No file ALC-" + repr(THIS_ALC) + "/GEN_FF/params.txt exists:")
                    print("Cannot post-process. Exiting.")
                    
                    exit()
                    
                # If needed, combine existing parameter files with newly generated one
                    
                if config.DO_HIERARCH:
                    
                    gen_ff.combine("GEN_FF/params.txt", config.HIERARCH_PARAM_FILES)                

                    helpers.run_bash_cmnd(config.CHIMES_POSTPRC + " hierarch.params.txt")
                    
                    helpers.run_bash_cmnd("mv  hierarch.params.txt.reduced GEN_FF/params.txt.reduced")
                    
                else:
                    helpers.run_bash_cmnd(config.CHIMES_POSTPRC + " GEN_FF/params.txt")
            
                restart_controller.update_file("SOLVE_AMAT: COMPLETE" + '\n')    
                helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "SOLVE_AMAT: COMPLETE ")
            
            else:
                restart_controller.update_file("SOLVE_AMAT: COMPLETE" + '\n')    
            
            
            
            ################################                
            # Extract/process/select clusters
            ################################
            
            if not restart_controller.CLUSTER_EXTRACTION:

                # Get a list of files from which to extract clusters
            
                traj_files = helpers.cat_to_var("GEN_FF/traj_list.dat")[1:]
            
            
                # Extract clusters from each file, save into own repo, list
            
                cat_xyzlist_cmnd    = ""
                cat_ts_xyzlist_cmnd = ""
            
            
                for i in range(len(traj_files)):
            
                    # Pre-process name
                    
                    traj_files[i] = traj_files[i].split()[1]
                    
                    print("Extracting clusters from file: ", traj_files[i])
                    
                    # Extract
            
                    cluster.generate_clusters(
                                traj_file   = "GEN_FF/" + traj_files[i].split()[0],
                                tight_crit  = config.TIGHT_CRIT,
                                loose_crit  = config.LOOSE_CRIT,
                                clu_code    = config.CLU_CODE,
                                compilation = "g++ -std=c++11 -O3")
                    
                    repo = "CFG_REPO-" + traj_files[i].split()[0]
                    
                    helpers.run_bash_cmnd("mv CFG_REPO " + repo)
                    
                    # list
                    
                    if config.MAX_CLUATM:
            
                        cluster.list_clusters(repo, config.ATOM_TYPES, config.MAX_CLUATM)
                    else:
                        cluster.list_clusters(repo, config.ATOM_TYPES)
                                        
                    helpers.run_bash_cmnd("mv xyzlist.dat    " + traj_files[i].split()[0] + ".xyzlist.dat"   )
                    helpers.run_bash_cmnd("mv ts_xyzlist.dat " + traj_files[i].split()[0] + ".ts_xyzlist.dat")
                    
                    cat_xyzlist_cmnd    += traj_files[i].split()[0] + ".xyzlist.dat "
                    cat_ts_xyzlist_cmnd += traj_files[i].split()[0] + ".ts_xyzlist.dat "
                    
                helpers.cat_specific("xyzlist.dat"   , cat_xyzlist_cmnd   .split())
                helpers.cat_specific("ts_xyzlist.dat", cat_ts_xyzlist_cmnd.split())

                helpers.run_bash_cmnd("rm -f " + cat_xyzlist_cmnd   )
                helpers.run_bash_cmnd("rm -f " + cat_ts_xyzlist_cmnd)
                
                restart_controller.update_file("CLUSTER_EXTRACTION: COMPLETE" + '\n')
                
                helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "CLUSTER_EXTRACTION: COMPLETE ")

            else:
                restart_controller.update_file("CLUSTER_EXTRACTION: COMPLETE" + '\n')
            
            if not restart_controller.CLUENER_CALC:

                # Compute cluster energies
            
                active_jobs = cluster.get_repo_energies(
                        base_runfile   = config.WORKING_DIR + "ALL_BASE_FILES/" + "run_md.cluster",
                        driver_dir     = config.DRIVER_DIR,
                        job_email      = config.HPC_EMAIL,
                        job_ppn        = str(config.HPC_PPN),
                        job_queue      = config.CALC_REPO_ENER_QUEUE,
                        job_walltime   = str(config.CALC_REPO_ENER_TIME),                    
                        job_cent_queue    = config.CALC_REPO_ENER_CENT_QUEUE,
                        job_cent_walltime = str(config.CALC_REPO_ENER_CENT_TIME), 
                        job_account    = config.HPC_ACCOUNT, 
                        job_system     = config.HPC_SYSTEM,
                        job_executable = config.MD_SER)    
                        
                helpers.wait_for_jobs(active_jobs, job_system = config.HPC_SYSTEM, verbose = True, job_name = "get_repo_energies")
            
                print(helpers.run_bash_cmnd("pwd"))
                print(helpers.run_bash_cmnd("ls -lrt"))    
            
                restart_controller.update_file("CLUENER_CALC: COMPLETE" + '\n')    
                
                helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "CLUENER_CALC: COMPLETE ")
                
            else:
                restart_controller.update_file("CLUENER_CALC: COMPLETE" + '\n')    
            
            
            if not restart_controller.CLU_SELECTION:
            
                # Generate cluster sub-selection and store in central repository
            
                gen_selections.cleanup_repo(THIS_ALC)
            
                gen_selections.gen_subset(
                        nsel     = config.MEM_NSEL, # Number of selections to make    
                        nsweep   = config.MEM_CYCL, # Number of MC sqeeps          
                        nbins    = config.MEM_BINS, # Number of histogram bins      
                        ecut     = config.MEM_ECUT, # Maximum energy to consider
                        seed     = config.SEED    ) # Seed for random number generator    
            
                gen_selections.populate_repo(THIS_ALC)

                repo = "CASE-" + str(THIS_CASE) + "_INDEP_" + str(THIS_INDEP) + "/CFG_REPO/"
                
                restart_controller.update_file("CLU_SELECTION: COMPLETE" + '\n')
                
                helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "CLU_SELECTION: COMPLETE ")
                
            else:
                restart_controller.update_file("CLU_SELECTION: COMPLETE" + '\n')

            
            ################################
            # Launch QM Cluster calculations
            ################################
            
            if not restart_controller.CLEANSETUP_QM:
            
                qm_driver.cleanup_and_setup(config.BULK_QM_METHOD, config.IGAS_QM_METHOD, ["all"], build_dir=".")
            
                restart_controller.update_file("CLEANSETUP_QM: COMPLETE" + '\n')
                
            else:
                restart_controller.update_file("CLEANSETUP_QM: COMPLETE" + '\n')
            
            
            if not restart_controller.INIT_QMJOB:    
    
                qm_driver.cleanup_and_setup(config.BULK_QM_METHOD, config.IGAS_QM_METHOD, ["all"], build_dir=".") # Always clean up, just in case    

                active_jobs = qm_driver.setup_qm(THIS_ALC,config.BULK_QM_METHOD, config.IGAS_QM_METHOD, 
                        ["all"], 
                        config.ATOM_TYPES,
                        THIS_CASE, 
                        SMEARING,
                        first_run      = True,
                        tight_crit     = config.TIGHT_CRIT,
                        loose_crit     = config.LOOSE_CRIT,
                        clu_code       = config.CLU_CODE,  
                        compilation    = "g++ -std=c++11 -O3",
                        basefile_dir   = config.QM_FILES,
                        VASP_exe       = config.VASP_EXE,
                        VASP_nodes     = config.VASP_NODES[THIS_CASE],
                        VASP_ppn       = config.VASP_PPN,
                        VASP_mem       = config.VASP_MEM,
                        VASP_time      = config.VASP_TIME,
                        VASP_queue     = config.VASP_QUEUE,
                        VASP_modules   = config.VASP_MODULES,
                        DFTB_nodes     = config.DFTB_NODES,  
                        DFTB_ppn       = config.DFTB_PPN,  
                        DFTB_mem       = config.DFTB_MEM,  
                        DFTB_time      = config.DFTB_TIME,   
                        DFTB_queue     = config.DFTB_QUEUE,  
                        DFTB_exe       = config.DFTB_EXE,    
                        DFTB_modules   = config.DFTB_MODULES,
                        CP2K_exe       = config.CP2K_EXE,
                        CP2K_nodes     = config.CP2K_NODES[THIS_CASE],
                        CP2K_ppn       = config.CP2K_PPN,
                        CP2K_mem       = config.CP2K_MEM,
                        CP2K_time      = config.CP2K_TIME,
                        CP2K_queue     = config.CP2K_QUEUE,
                        CP2K_modules   = config.CP2K_MODULES,
                        CP2K_data_dir  = config.CP2K_DATADIR,
                        Gaussian_exe   = config.GAUS_EXE,
                        Gaussian_scr   = config.GAUS_SCR,
                        Gaussian_nodes = config.GAUS_NODES,
                        Gaussian_mem   = config.GAUS_MEM,
                        Gaussian_ppn   = config.GAUS_PPN,
                        Gaussian_time  = config.GAUS_TIME,
                        Gaussian_queue = config.GAUS_QUEUE,       
                        LMP_exe        = config.LMP_EXE,
                        LMP_units      = config.LMP_UNITS,
                        LMP_nodes      = config.LMP_NODES,
                        LMP_ppn        = config.LMP_PPN,
                        LMP_mem        = config.LMP_MEM,
                        LMP_time       = config.LMP_TIME,
                        LMP_queue      = config.LMP_QUEUE,
                        LMP_modules    = config.LMP_MODULES,                      
                        job_ppn        = config.HPC_PPN,
                        job_account    = config.HPC_ACCOUNT,
                        job_system     = config.HPC_SYSTEM,
                        job_email      = config.HPC_EMAIL)

                helpers.wait_for_jobs(active_jobs, job_system = config.HPC_SYSTEM, verbose = True, job_name = "setup_qm")

                restart_controller.update_file("INIT_QMJOB: COMPLETE" + '\n')    
                
                helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "INIT_QMJOB: COMPLETE ")        
                
            else:
                restart_controller.update_file("INIT_QMJOB: COMPLETE" + '\n')
            
            # Check that the job was complete
            
            if not restart_controller.ALL_QMJOBS:

                while True:

                    active_jobs = qm_driver.continue_job(config.BULK_QM_METHOD, config.IGAS_QM_METHOD, 
                            ["all"], 
                            job_system     = config.HPC_SYSTEM)
                            
                    print("active jobs: ", active_jobs)            
                            
                    if len(active_jobs) > 0:
                
                        print("waiting for restarted qm job.")
                
                        helpers.wait_for_jobs(active_jobs, job_system = config.HPC_SYSTEM, verbose = True, job_name = "setup_qm - restarts")
                    else:
                        print("All jobs are complete")
                        break        
            
            
                restart_controller.update_file("ALL_QMJOBS: COMPLETE" + '\n')
                
                helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "ALL_QMJOBS: COMPLETE ")
                
            else:
                restart_controller.update_file("ALL_QMJOBS: COMPLETE" + '\n')
            
            
            total_failed = qm_driver.check_convergence(THIS_ALC, config.BULK_QM_METHOD, config.IGAS_QM_METHOD, 
                                    config.NO_CASES,
                                    ["all"])
                                    
            print("Detected",total_failed,"unconverged QM jobs")    
                        
            if total_failed > 0:
            
                # Check that the job was complete
            
                if not restart_controller.ALL_FAILED_QMJOBS:

                    while True:

                        active_jobs = qm_driver.continue_job(config.BULK_QM_METHOD, config.IGAS_QM_METHOD, 
                                ["all"], 
                                job_system     = config.HPC_SYSTEM)
                                
                        print("active jobs: ", active_jobs)            
                                
                        if len(active_jobs) > 0:
                    
                            print("waiting for re-run qm job.")
                    
                            helpers.wait_for_jobs(active_jobs, job_system = config.HPC_SYSTEM, verbose = True, job_name = "setup_qm - re-runs")
                        else:
                            print("All jobs are complete")
                            break        
            
            
                    restart_controller.update_file("ALL_FAILED_QMJOBS: COMPLETE" + '\n')
                    
                    helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "ALL_FAILED_QMJOBS: COMPLETE ")        
            
            else:
            
                restart_controller.update_file("ALL_FAILED_QMJOBS: COMPLETE" + '\n')
                
                
            if not restart_controller.THIS_ALC:

                # Post-process the qm jobs
            
                print("post-processing...")    
            
                qm_driver.post_process(config.BULK_QM_METHOD, config.IGAS_QM_METHOD, ["all"], "ENERGY",
                    vasp_postproc = config.VASP_POSTPRC,
                    dftb_postproc = config.DFTB_POSTPRC, 
                    cp2k_postproc = config.CP2K_POSTPRC,
                    lmp_postproc  = config.LMP_POSTPRC,
                    gaus_reffile  = config.GAUS_REF)
                    # gaus_postproc = config.GAUS_POSTPRC) -- this is unused

            os.chdir("..")
            
            print("ALC-", THIS_ALC, "is complete")    
            
            restart_controller.update_file("THIS_ALC: COMPLETE" + '\n')
            
            helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "THIS_ALC: COMPLETE ")        
            
        else:
        
            if not restart_controller.BUILD_AMAT: # Then we haven't even begun this ALC

                # Set up/move into the ALC directory
            
                helpers.run_bash_cmnd("rm -rf ALC-" + str(THIS_ALC))
                helpers.run_bash_cmnd("mkdir  ALC-" + str(THIS_ALC))
            
            os.chdir("ALC-" + str(THIS_ALC))
            
            qm_all_path = ""
            qm_20F_path = ""
            
            if config.IGAS_QM_METHOD == "VASP":
                qm_all_path = config.WORKING_DIR + "/ALC-" + repr(THIS_ALC-1) + "/VASP-all/"
            elif config.IGAS_QM_METHOD == "DFTB+":
                qm_all_path = config.WORKING_DIR + "/ALC-" + repr(THIS_ALC-1) + "/DFTB-all/"
            elif config.IGAS_QM_METHOD == "CP2K":
                qm_all_path = config.WORKING_DIR + "/ALC-" + repr(THIS_ALC-1) + "/CP2K-all/"
            elif config.IGAS_QM_METHOD == "Gaussian":
                qm_all_path = config.WORKING_DIR + "/ALC-" + repr(THIS_ALC-1) + "/GAUS-all/"
            elif config.IGAS_QM_METHOD == "LMP":
                qm_all_path = config.WORKING_DIR + "/ALC-" + repr(THIS_ALC-1) + "/LMP-all/"                
            else:
                print("Error in main driver while building Amat: unkown IGAS QM method:", config.IGAS_QM_METHOD)
                exit()
            
            if THIS_ALC > 1:
            
                if config.BULK_QM_METHOD == "VASP":
                    qm_20F_path = config.WORKING_DIR + "/ALC-" + repr(THIS_ALC-1) + "/VASP-20/"
                elif config.BULK_QM_METHOD == "DFTB+":
                    qm_20F_path = config.WORKING_DIR + "/ALC-" + repr(THIS_ALC-1) + "/DFTB-20/"  
                elif config.BULK_QM_METHOD == "CP2K":
                    qm_20F_path = config.WORKING_DIR + "/ALC-" + repr(THIS_ALC-1) + "/CP2K-20/"   
                elif config.BULK_QM_METHOD == "LMP":
                    qm_20F_path = config.WORKING_DIR + "/ALC-" + repr(THIS_ALC-1) + "/LMP-20/"          
                else:
                    print("Error in main driver while building Amat: unkown BULK QM method:", config.BULK_QM_METHOD)
                    exit()

            if not restart_controller.BUILD_AMAT:
            
                do_stress = False
                
                if THIS_ALC >= config.USE_AL_STRS:
                    do_stress = True
                
                if (not config.DO_CLUSTER) and (THIS_ALC == 1):    
                
                    active_jobs = gen_ff.build_amat(THIS_ALC,
                            do_hierarch        = config.DO_HIERARCH,
			    hierarch_method    = config.HIERARCH_METHOD,
                            hierarch_files     = config.HIERARCH_PARAM_FILES,
                            hierarch_exe       = config.HIERARCH_EXE,
                            do_correction      = config.FIT_CORRECTION,
                            correction_method  = config.CORRECTED_TYPE,
                            correction_files   = config.CORRECTED_TYPE_FILES,
                            correction_exe     = config.CORRECTED_TYPE_EXE,                            
                            correction_temps   = config.CORRECTED_TEMPS_BY_FILE,                            
                            n_hyper_sets       = config.N_HYPER_SETS,
                            do_cluster         = config.DO_CLUSTER,
                            prev_gen_path      = config.ALC0_FILES,
                            job_email          = config.HPC_EMAIL,
                            job_ppn            = str(config.HPC_PPN),
                            job_nodes          = config.CHIMES_BUILD_NODES,
                            job_walltime       = config.CHIMES_BUILD_TIME,    
                            job_queue          = config.CHIMES_BUILD_QUEUE,        
                            job_account        = config.HPC_ACCOUNT, 
                            job_system         = config.HPC_SYSTEM,
                            job_executable     = config.CHIMES_LSQ,
                            job_modules        = config.CHIMES_LSQ_MODULES)    
                else:
            
                    active_jobs = gen_ff.build_amat(THIS_ALC, 
                        prev_qm_all_path = qm_all_path,
                        prev_qm_20_path  = qm_20F_path,
                        do_hierarch      = config.DO_HIERARCH,
			hierarch_method  = config.HIERARCH_METHOD,
                        hierarch_files   = config.HIERARCH_PARAM_FILES,    
                        hierarch_exe     = config.HIERARCH_EXE, #config.MD_SER,
                        do_correction    = config.FIT_CORRECTION,
                        correction_method= config.CORRECTED_TYPE,
                        correction_files = config.CORRECTED_TYPE_FILES,
                        correction_exe   = config.CORRECTED_TYPE_EXE,                            
                        correction_temps = config.CORRECTED_TEMPS_BY_FILE,  
                        n_hyper_sets     = config.N_HYPER_SETS,                      
                        do_cluster       = config.DO_CLUSTER,
                        include_stress   = do_stress,    
                        stress_style     = config.STRS_STYLE,
                        job_email        = config.HPC_EMAIL,
                        job_ppn          = str(config.HPC_PPN),
                        job_nodes        = config.CHIMES_BUILD_NODES,
                        job_walltime     = config.CHIMES_BUILD_TIME,    
                        job_queue        = config.CHIMES_BUILD_QUEUE,                        
                        job_account      = config.HPC_ACCOUNT, 
                        job_system       = config.HPC_SYSTEM,
                        job_executable   = config.CHIMES_LSQ,
                        job_modules      = config.CHIMES_LSQ_MODULES
                        )
            
                if len(active_jobs) == 1:
                    helpers.wait_for_job(active_jobs[0], job_system = config.HPC_SYSTEM, verbose = True, job_name = "build_amat")
                else:
                    helpers.wait_for_jobs(active_jobs, job_system = config.HPC_SYSTEM, verbose = True, job_name = "build_amat")                    
            
                restart_controller.update_file("BUILD_AMAT: COMPLETE" + '\n')
                
                helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "BUILD_AMAT: COMPLETE ")
            else:
                restart_controller.update_file("BUILD_AMAT: COMPLETE" + '\n')
                        
    
            if not restart_controller.SOLVE_AMAT:    
            
                # Check whether we have previously started 
                # only works for dlasso/dlars... for all other algorithms, assumes false
            
                if not gen_ff.solve_amat_started(config.N_HYPER_SETS): 
                    print("Starting solve_amat from scratch")
            
                    active_job = gen_ff.solve_amat(THIS_ALC, 
                        do_cluster         = config.DO_CLUSTER,
                        weights_set_alc_0  = config.WEIGHTS_SET_ALC_0,
                        weights_alc_0      = config.WEIGHTS_ALC_0,                        
                        weights_force      = config.WEIGHTS_FORCE,
                        weights_force_gas  = config.WEIGHTS_FGAS,
                        weights_energy     = config.WEIGHTS_ENER,
                        weights_energy_gas = config.WEIGHTS_EGAS,
                        weights_stress     = config.WEIGHTS_STRES,
                        regression_alg     = config.REGRESS_ALG,
                        regression_nrm     = config.REGRESS_NRM,
                        regression_var     = config.REGRESS_VAR,  
			            n_hyper_sets       = config.N_HYPER_SETS,  
                        job_email          = config.HPC_EMAIL,                    
                        job_ppn            = config.CHIMES_SOLVE_PPN,
                        node_ppn           = config.HPC_PPN,
                        job_nodes          = config.CHIMES_SOLVE_NODES,
                        job_walltime       = config.CHIMES_SOLVE_TIME,    
                        job_queue          = config.CHIMES_SOLVE_QUEUE,                            
                        job_account        = config.HPC_ACCOUNT, 
                        job_system         = config.HPC_SYSTEM,
                        job_executable     = config.CHIMES_SOLVER,
                        job_modules        = config.CHIMES_LSQ_MODULES
                        )    
                        
                    helpers.wait_for_job(active_job, job_system = config.HPC_SYSTEM, verbose = True, job_name = "solve_amat")
                
                # Check whether the amat_solve job has completed and keep track of how many times it has run

                n_restarts = 0
                print("Prior to solve_amat_completed")
                while not gen_ff.solve_amat_completed():
                
                    n_restarts += 1
    
                    print("solve amat job incomplete... restarting for the ", n_restarts, "st/nd/th time")
                    
                    active_job = gen_ff.restart_solve_amat(THIS_ALC,
                        regression_alg     = config.REGRESS_ALG,
                        regression_nrm     = config.REGRESS_NRM,
                        regression_var     = config.REGRESS_VAR,    
                        job_email          = config.HPC_EMAIL,        
                        job_ppn            = config.CHIMES_SOLVE_PPN,
                        node_ppn           = config.HPC_PPN,    
                        job_nodes          = config.CHIMES_SOLVE_NODES,
                        job_walltime       = config.CHIMES_SOLVE_TIME,    
                        job_queue          = config.CHIMES_SOLVE_QUEUE,    
                        job_account        = config.HPC_ACCOUNT, 
                        job_system         = config.HPC_SYSTEM,
                        job_executable     = config.CHIMES_SOLVER,
                        job_modules        = config.CHIMES_LSQ_MODULES
                        )    
                    
                    helpers.wait_for_job(active_job, job_system = config.HPC_SYSTEM, verbose = True, job_name = "restart_solve_amat")
                
                if config.N_HYPER_SETS > 1:
                
                    gen_ff.parse_hyper_params(
                        n_hyper_sets     = config.N_HYPER_SETS, 
                        job_executable   = config.CHIMES_SOLVER
                        )
                    
                
                #if n_restarts > 0: # Then we need to manually build the parameter file
                
                if (not os.path.isfile("GEN_FF/params.txt")) and (config.N_HYPER_SETS == 1):
                    print("ERROR: No file ALC-" + repr(THIS_ALC) + "/GEN_FF/params.txt exists:")
                    print("Cannot post-process. Exiting.")
                    
                    exit()
                elif config.N_HYPER_SETS > 1:
                
                    param_files =  glob.glob("GEN_FF-*/params.txt")
                    
                    if len(param_files) < config.N_HYPER_SETS:
                    
                        print("ERROR: Didn't find expected number of parameter files (",config.N_HYPER_SETS, "):")
                        print(param_files)
                        print("Cannot post-process. Exiting.")
                        
                        exit()
  
                    
                if config.DO_HIERARCH and config.N_HYPER_SETS == 1:
                    gen_ff.combine("GEN_FF/params.txt", config.HIERARCH_PARAM_FILES)    
                    helpers.run_bash_cmnd(config.CHIMES_POSTPRC + " hierarch.params.txt")                    
                    helpers.run_bash_cmnd("mv  hierarch.params.txt.reduced GEN_FF/params.txt.reduced")                

                elif config.N_HYPER_SETS > 1:
                
                    for i in range(config.N_HYPER_SETS):
                        helpers.run_bash_cmnd(config.CHIMES_POSTPRC + " GEN_FF-" + str(i) + "/params.txt")
                else:
                    
                    helpers.run_bash_cmnd(config.CHIMES_POSTPRC + " GEN_FF/params.txt")
            
                restart_controller.update_file("SOLVE_AMAT: COMPLETE" + '\n')    
                helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "SOLVE_AMAT: COMPLETE ")                    
                
                restart_controller.update_file("SOLVE_AMAT: COMPLETE" + '\n')    
                
                helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "SOLVE_AMAT: COMPLETE ")
            else:
                restart_controller.update_file("SOLVE_AMAT: COMPLETE" + '\n')    
            
            ################################                
            # Run MD
            ################################
            
            
            # ... May want to consider making speciation optional ... can add another key word that allows the user to set up different 
            #    types of post-processing jobs
            
            
            if not restart_controller.RUN_MD:
                    
                # Run the MD/cluster jobs
            
                active_jobs = []
                
                #print "running for cases:", config.NO_CASES

                for THIS_CASE in range(config.NO_CASES):

                    active_job = run_md.run_md(THIS_ALC, THIS_CASE, THIS_INDEP, config.MD_STYLE,
                        basefile_dir   = config.MDFILES, 
                        driver_dir     = config.DRIVER_DIR,
                        penalty_pref   = 1.0E6,        
                        penalty_dist   = 0.02,         
                        n_hyper_sets   = config.N_HYPER_SETS,     
                        chimes_exe     = config.MD_SER,
                        job_name       = "ALC-"+ str(THIS_ALC) +"-md-c" + str(THIS_CASE) +"-i" + str(THIS_INDEP),
                        job_email      = config.HPC_EMAIL,            
                        job_ppn        = config.HPC_PPN,            
                        job_nodes      = config.MD_NODES[THIS_CASE],
                        job_walltime   = config.MD_TIME [THIS_CASE],      
                        job_queue      = config.MD_QUEUE[THIS_CASE],      
                        job_account    = config.HPC_ACCOUNT, 
                        job_executable = config.MD_MPI,     
                        job_system     = config.HPC_SYSTEM,       
                        job_file       = "run.cmd",
                        job_modules    = config.MD_MODULES
                        )
                        
        
                    active_jobs.append(active_job.split()[0])    
                                    
                helpers.wait_for_jobs(active_jobs, job_system = config.HPC_SYSTEM, verbose = True, job_name = "run_md")

                restart_controller.update_file("RUN_MD: COMPLETE" + '\n')
                
                helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "RUN_MD: COMPLETE ")
            else:
                restart_controller.update_file("RUN_MD: COMPLETE" + '\n')
                        
            if not restart_controller.POST_PROC:
            
                for THIS_CASE in range(config.NO_CASES):    
            
                    # Post-process the MD job
            
                    run_md.post_proc(THIS_ALC, THIS_CASE, THIS_INDEP, config.MD_STYLE, 
                        config.MOLANAL_SPECIES,
                        basefile_dir   = config.MDFILES, 
                        driver_dir     = config.DRIVER_DIR,
                        penalty_pref   = config.CHIMES_PEN_PREFAC,      
                        penalty_dist   = config.CHIMES_PEN_DIST,          
                        molanal_dir    = config.MOLANAL, 
                        local_python   = config.HPC_PYTHON,     
                        do_cluster     = config.DO_CLUSTER,    
                        tight_crit     = config.TIGHT_CRIT,    
                        loose_crit     = config.LOOSE_CRIT,    
                        clu_code       = config.CLU_CODE,      
                        compilation    = "g++ -std=c++11 -O3")

                restart_controller.update_file("POST_PROC: COMPLETE" + '\n')
                
                helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "POST_PROC: COMPLETE ")
            else:
                restart_controller.update_file("POST_PROC: COMPLETE" + '\n')    
                
                
            if config.DO_CLUSTER:
            
                if not restart_controller.CLUSTER_EXTRACTION:
                
                    # list ... remember, we only do clustering/active learning on a single indep (0)
                
                    cat_xyzlist_cmnd    = ""
                    cat_ts_xyzlist_cmnd = ""        
                
                    for THIS_CASE in range(config.NO_CASES):
                            
                        repo = "CASE-" + str(THIS_CASE) + "_INDEP_" + str(THIS_INDEP) + "/CFG_REPO/"
   
                        if config.MAX_CLUATM:
                
                            cluster.list_clusters(repo, config.ATOM_TYPES, config.MAX_CLUATM)
                        else:
                            cluster.list_clusters(repo, config.ATOM_TYPES)        
                
                            helpers.run_bash_cmnd("mv xyzlist.dat     " + "CASE-" + str(THIS_CASE) + ".xyzlist.dat"   )
                            helpers.run_bash_cmnd("mv ts_xyzlist.dat " + "CASE-" + str(THIS_CASE) + ".ts_xyzlist.dat")
                
                            cat_xyzlist_cmnd    += "CASE-" + str(THIS_CASE) + ".xyzlist.dat "
                            cat_ts_xyzlist_cmnd += "CASE-" + str(THIS_CASE) + ".ts_xyzlist.dat "
                
                    helpers.cat_specific("xyzlist.dat"   , cat_xyzlist_cmnd   .split())
                    helpers.cat_specific("ts_xyzlist.dat", cat_ts_xyzlist_cmnd.split())
                
                    helpers.run_bash_cmnd("rm -f " + cat_xyzlist_cmnd   )
                    helpers.run_bash_cmnd("rm -f " + cat_ts_xyzlist_cmnd)
                    
                    restart_controller.update_file("CLUSTER_EXTRACTION: COMPLETE" + '\n')    
                    
                    helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "CLUSTER_EXTRACTION: COMPLETE ")                
                else:
                    restart_controller.update_file("CLUSTER_EXTRACTION: COMPLETE" + '\n')                    
                
                        
                if not restart_controller.CLUENER_CALC:
                
                    # Compute cluster energies
                
                    gen_selections.cleanup_repo(THIS_ALC)    
                
                    active_jobs = cluster.get_repo_energies(
                            calc_central   = True,
                            base_runfile   = config.WORKING_DIR + "ALL_BASE_FILES/" + "run_md.cluster",
                            driver_dir     = config.DRIVER_DIR,
                            job_email      = config.HPC_EMAIL,
                            job_ppn        = str(config.HPC_PPN),
                            job_queue      = config.CALC_REPO_ENER_QUEUE,
                            job_walltime   = str(config.CALC_REPO_ENER_TIME),                  
                            job_cent_queue    = config.CALC_REPO_ENER_CENT_QUEUE,
                            job_cent_walltime = str(config.CALC_REPO_ENER_CENT_TIME), 
                            job_account    = config.HPC_ACCOUNT, 
                            job_system     = config.HPC_SYSTEM,
                            job_executable = config.MD_SER)    
                            
                    helpers.wait_for_jobs(active_jobs, job_system = config.HPC_SYSTEM, verbose = True, job_name = "get_repo_energies")
                
                    restart_controller.update_file("CLUENER_CALC: COMPLETE" + '\n')    
                    
                    helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "CLUENER_CALC: COMPLETE ")    
                else:
                    restart_controller.update_file("CLUENER_CALC: COMPLETE" + '\n')    
                
                
                if not restart_controller.CLU_SELECTION:
                
                    # Generate cluster sub-selection and store in central repository
                
                    gen_selections.gen_subset(
                             repo      = "../CENTRAL_REPO/full_repo.energies_normed",
                             nsel      = config.MEM_NSEL, # Number of selections to make    
                             nsweep   = config.MEM_CYCL, # Number of MC sqeeps           
                             nbins    = config.MEM_BINS, # Number of histogram bins      
                             ecut      = config.MEM_ECUT) # Maximum energy to consider    
                             
                    gen_selections.populate_repo(THIS_ALC)   
                             
                    restart_controller.update_file("CLU_SELECTION: COMPLETE" + '\n')
                    
                    helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "CLU_SELECTION: COMPLETE ")
                else:
                    restart_controller.update_file("CLU_SELECTION: COMPLETE" + '\n')
                                     
                
            ################################
            # Launch QM
            ################################
            
            # Note: If multiple cases are being used, only run clean/setup once!
            
            tasks = ["20"]
            
            if config.DO_CLUSTER:
                tasks = ["20","all"]
            
            if not restart_controller.CLEANSETUP_QM:
            
                qm_driver.cleanup_and_setup(config.BULK_QM_METHOD, config.IGAS_QM_METHOD, tasks, build_dir=".")
            
                restart_controller.update_file("CLEANSETUP_QM: COMPLETE" + '\n')    
            else:
                restart_controller.update_file("CLEANSETUP_QM: COMPLETE" + '\n')
                           
            if not restart_controller.INIT_QMJOB:    
            
                active_jobs = []

                qm_driver.cleanup_and_setup(config.BULK_QM_METHOD, config.IGAS_QM_METHOD, tasks, build_dir=".")
                
                for THIS_CASE in range(config.NO_CASES):

                    qm_driver  .cleanup_and_setup(config.BULK_QM_METHOD, config.IGAS_QM_METHOD, tasks, THIS_CASE, build_dir=".") # Always clean up, just in case
                                        
                    active_job = qm_driver.setup_qm(THIS_ALC,config.BULK_QM_METHOD, config.IGAS_QM_METHOD,
                        tasks, 
                        config.ATOM_TYPES,
                        THIS_CASE, 
                        SMEARING,
                        first_run      = True,
                        tight_crit     = config.TIGHT_CRIT,
                        loose_crit     = config.LOOSE_CRIT,
                        clu_code       = config.CLU_CODE,  
                        compilation    = "g++ -std=c++11 -O3",
                        basefile_dir   = config.QM_FILES,
                        VASP_exe       = config.VASP_EXE,
                        VASP_nodes     = config.VASP_NODES[THIS_CASE],
                        VASP_ppn       = config.VASP_PPN,
                        VASP_mem       = config.VASP_MEM,
                        VASP_time      = config.VASP_TIME,
                        VASP_queue     = config.VASP_QUEUE,
                        VASP_modules   = config.VASP_MODULES,
                        DFTB_exe       = config.DFTB_EXE,
                        DFTB_nodes     = config.DFTB_NODES,
                        DFTB_ppn       = config.DFTB_PPN,
                        DFTB_mem       = config.DFTB_MEM,
                        DFTB_time      = config.DFTB_TIME,
                        DFTB_modules   = config.DFTB_MODULES,
                        DFTB_queue     = config.DFTB_QUEUE,
                        CP2K_exe       = config.CP2K_EXE,
                        CP2K_nodes     = config.CP2K_NODES[THIS_CASE],
                        CP2K_ppn       = config.CP2K_PPN,
                        CP2K_mem       = config.CP2K_MEM,
                        CP2K_time      = config.CP2K_TIME,
                        CP2K_queue     = config.CP2K_QUEUE,
                        CP2K_modules   = config.CP2K_MODULES,
                        CP2K_data_dir  = config.CP2K_DATADIR,  
                        LMP_exe     = config.LMP_EXE,
                        LMP_units   = config.LMP_UNITS,
                        LMP_nodes   = config.LMP_NODES,
                        LMP_ppn     = config.LMP_PPN,
                        LMP_mem     = config.LMP_MEM,
                        LMP_time    = config.LMP_TIME,
                        LMP_queue   = config.LMP_QUEUE,
                        LMP_modules = config.LMP_MODULES,                                                                       
                        Gaussian_exe   = config.GAUS_EXE,
                        Gaussian_scr   = config.GAUS_SCR,
                        Gaussian_nodes = config.GAUS_NODES,
                        Gaussian_ppn   = config.GAUS_PPN,
                        Gaussian_mem   = config.GAUS_MEM,
                        Gaussian_time  = config.GAUS_TIME,
                        Gaussian_queue = config.GAUS_QUEUE,
                        job_ppn        = config.HPC_PPN,
                        job_account    = config.HPC_ACCOUNT,
                        job_system     = config.HPC_SYSTEM,
                        job_email      = config.HPC_EMAIL)
                                                    
                    active_jobs += active_job

                helpers.wait_for_jobs(active_jobs, job_system = config.HPC_SYSTEM, verbose = True, job_name = "setup_qm")
            
                restart_controller.update_file("INIT_QMJOB: COMPLETE" + '\n')
                
                helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "INIT_QMJOB: COMPLETE ")
            else:
                restart_controller.update_file("INIT_QMJOB: COMPLETE" + '\n')

        
            if not restart_controller.ALL_QMJOBS:

                while True:    # Check that the job was complete
                
                    active_jobs = []
                
                    for THIS_CASE in range(config.NO_CASES):

                        active_job = qm_driver.continue_job(config.BULK_QM_METHOD, config.IGAS_QM_METHOD, tasks, THIS_CASE, 
                                job_system = config.HPC_SYSTEM)
                                
                        active_jobs += active_job
                                
                    print("active jobs: ", active_jobs)            
                                
                    if len(active_jobs) > 0:
                    
                        print("waiting for restarted qm job.")
                    
                        helpers.wait_for_jobs(active_jobs, job_system = config.HPC_SYSTEM, verbose = True, job_name = "setup_qm - restarts")
                    else:
                        print("All jobs are complete")
                        break    
                        
                restart_controller.update_file("ALL_QMJOBS: COMPLETE" + '\n')
                
                helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "ALL_QMJOBS: COMPLETE ")
            else:
                restart_controller.update_file("ALL_QMJOBS: COMPLETE" + '\n')
                
            total_failed = qm_driver.check_convergence(THIS_ALC, config.BULK_QM_METHOD, config.IGAS_QM_METHOD, config.NO_CASES, tasks)
            
            print("Detected",total_failed,"unconverged QM jobs")    
                                        
            if total_failed > 0:
            
                # Check that the job was complete
            
                if not restart_controller.ALL_FAILED_QMJOBS:
                
                    while True:    # Check that the job was complete
                
                        active_jobs = []
                
                        for THIS_CASE in range(config.NO_CASES):

                            # FIXED
                            active_job = qm_driver.continue_job(config.BULK_QM_METHOD, config.IGAS_QM_METHOD, tasks, THIS_CASE,
                                job_system = config.HPC_SYSTEM)
                                    
                            active_jobs += active_job
                                    
                        print("active jobs: ", active_jobs)            
                                    
                        if len(active_jobs) > 0:
                        
                            print("waiting for re-run qm jobs.")
                        
                            helpers.wait_for_jobs(active_jobs, job_system = config.HPC_SYSTEM, verbose = True, job_name = "setup_qm - re-runs")
                        else:
                            print("All jobs are complete")
                            break    
                            
                    restart_controller.update_file("ALL_FAILED_QMJOBS: COMPLETE" + '\n')

                    helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "ALL_FAILED_QMJOBS: COMPLETE ")
            else:
            
                restart_controller.update_file("ALL_FAILED_QMJOBS: COMPLETE" + '\n')

            
            if not restart_controller.THIS_ALC:

                # Post-process the vasp/DFTB jobs
            
                print("post-processing...")    

                if config.DO_CLUSTER:
                
                    # Do all first... extract only forces and energies
                
                    qm_driver.post_process(config.BULK_QM_METHOD, config.IGAS_QM_METHOD, ["all"], "ENERGY", config.NO_CASES,
                        vasp_postproc = config.VASP_POSTPRC,
                        dftb_postproc = config.DFTB_POSTPRC,
                        cp2k_postproc = config.CP2K_POSTPRC,
                        lmp_postproc  = config.LMP_POSTPRC,
                        gaus_reffile  = config.GAUS_REF)
                        #gaus_postproc = config.GAUS_POSTPRC) -- this is unused
                        
                # Now do full frames... may or may not need to extract stress tensors as well. This descision is based on whether the *next* ALC requires stresses!

                extract = "ENERGY "
                
                if THIS_ALC >= (config.USE_AL_STRS-1):

                    if config.STRS_STYLE == "DIAG":
                        extract += " STRESS"
                    else: 
                        extract += " ALLSTR"
                
                qm_driver.post_process(config.BULK_QM_METHOD, config.IGAS_QM_METHOD, ["20"], extract, config.NO_CASES,
                    vasp_postproc = config.VASP_POSTPRC,
                    dftb_postproc = config.DFTB_POSTPRC,
                    cp2k_postproc = config.CP2K_POSTPRC,
                    lmp_postproc  = config.LMP_POSTPRC,
                    gaus_reffile  = config.GAUS_REF)
                    #gaus_postproc = config.GAUS_POSTPRC) -- this is unused
                        
                        
            os.chdir("..")
            
            print("ALC-", THIS_ALC, "is complete")    
            
            restart_controller.update_file("THIS_ALC: COMPLETE" + '\n')    

            helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "THIS_ALC: COMPLETE ")
                    

if __name__=='__main__':

    """ 
    
    Allows commandline calls to main().
    
              
    """    
    
    main(sys.argv[1:])
