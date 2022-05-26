# Global (python) modules

import os
import sys

# Local modules

import helpers
import run_md

# Allow config file to be read from local directory

local_path = os.path.normpath(helpers.run_bash_cmnd("pwd").rstrip())
sys.path.append(local_path)
import config  # User-specified "global" vars


def main(args):

    """ 
    
    Code Author: Rebecca K Lindsey (RKL) - 2019

    Utility for Active Learning Driver: Launches independent MD simulations

    Usage: unbuffer python launch_indeps.py ALC 15 INDEPS 1 2 3 4 5 6 7 | tee launch_indeps.log 

    Notes: 
    
           - Uses the same config.py file as AL driver main.py
           - Expects to be run from the ALC base folder, i.e. 
             where ALC-* directories and config.py are located
           
    To Do: 
    
           - To do goes here       
    
    """    
    
    ################################
    # Initialize vars
    ################################    
    
    if os.path.normpath(config.WORKING_DIR) != local_path:
    
        print("Error: this script was not run from config.WORKING_DIR!")
        print("config.WORKING_DIR:",config.WORKING_DIR)
        print("local path:        ",local_path)
        print("Exiting.")
        
        exit()
    
    print("The following has been set as the working directory:")
    print('\t', config.WORKING_DIR)    
    
    if (args[0] != "ALC") or (len(args)<4):
        print("Syntax error. Utility should be called like:")
        print("unbuffer python launch_indeps.py ALC 15 INDEPS 1 2 3 4 5 6 7 | tee launch_indeps.log")
        print("Received the following args instead:")
        print(' '.join(args))
        exit()
        
    if not any(x.isdigit() for x in args[1]): # Make sure the second user arg is a number
        print("Syntax error. \"ALC\" must be followed by a number")
        print("Received the following args instead:")
        print(' '.join(args))
        exit()    
            
    if args[2] != "INDEPS":
        print("Syntax error. Third argument should be \"INDEPS\":")
        print("Received the following args instead:")
        print(' '.join(args))    
        exit()
        
    for i in range(3,len(args)):
        if not any(x.isdigit() for x in args[i]): # Make sure the second user arg is a number
            print("Syntax error. \"INDEPS\" must be followed by a set of numbers")
            print("Received the following args instead:")
            print(' '.join(args))
            exit()    
            
    
    THIS_ALC = int(args[1])
    INDEPLST = list(map(int,args[3:]))
    
    print("Launching independent ChIMES MD simulations for ALC:", THIS_ALC)
    print("Will launch the following independent simulations:",  INDEPLST)

    
    ################################
    # Pre-process user specified variables
    ################################

    config.ATOM_TYPES.sort()

    if config.EMAIL_ADD:
        EMAIL_ADD = config.EMAIL_ADD    
        
        
    ################################
    ################################
    # Begin launching simulations
    ################################
    ################################        

    os.chdir("ALC-" + args[1])
    #print "\nCurrently in the following directory:",helpers.run_bash_cmnd("pwd")        
    
    for THIS_CASE in range(config.NO_CASES):
    
        for THIS_INDEP in INDEPLST:
        


            active_job = run_md.run_md(THIS_ALC, THIS_CASE, THIS_INDEP,
                basefile_dir   = config.CHIMES_MDFILES, 
                driver_dir     = config.DRIVER_DIR,
                penalty_pref   = 1.0E6,        
                penalty_dist   = 0.02,         
                job_name       = "ALC-"+ str(THIS_ALC) +"-md-c" + str(THIS_CASE) +"-i" + str(THIS_INDEP),
                job_email      = config.HPC_EMAIL,            
                job_ppn        = config.HPC_PPN,            
                job_nodes      = config.CHIMES_MD_NODES,
                job_walltime   = config.CHIMES_MD_TIME,      
                job_queue      = config.CHIMES_MD_QUEUE,      
                job_account    = config.HPC_ACCOUNT, 
                job_executable = config.CHIMES_MD_MPI,     
                job_system     = "slurm",       
                job_file       = "run.cmd")
        
        
            print("\tLaunched case",THIS_CASE,"indep",THIS_INDEP,"with job id:",active_job.split()[0])
            
            #print "\nEnding in the following directory:",helpers.run_bash_cmnd("pwd")
    
        print("")

    #print "\nEnding big loop in the following directory:",helpers.run_bash_cmnd("pwd")
    
    print("All tasks complete.\n")
            
            









if __name__=='__main__':

    """ 
    
    Allows commandline calls to main().
    
              
    """    
    
    main(sys.argv[1:])
