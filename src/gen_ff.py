# Global (python) modules

import os.path
import os
import glob # Warning: glob is unsorted... set my_list = sorted(glob.glob(<str>)) if sorting needed
import copy
import math as m

# Local modules

import helpers
import hierarch
import modify_FES


def combine(to_file, from_files):

    """
    
    Combines existing parameter files into a freshly built parameter file
    
    Usage: combine(<to (new) param file>, [<supplement param file 1>, <supplement param file 2>, <supplement param file 3>, ...) 
    
    """

    hierarch.main(base_file=to_file, new_files=from_files)

def subtract(**kwargs):

    """
    
    Subtracts force, energy, and stress contributions from a list of ChIMES parameter files,
    from a list of trajectory files
    
    Usage: subtract("/path/to/chimes_md-ser", "CHIMES", ["traj-1.xyzf", "traj-2.xyzf",...], ["params.C.txt","params.H.txt", "params.CH.txt",...]
    
    """    
    
    ################################
    # 0. Set up an argument parser
    ################################
    
    default_keys   = [""]*5
    default_values = [""]*5


    default_keys[0 ] = "md_driver"       ; default_values[0 ] = None      # MD code executable to use when evaluating interactions
    default_keys[1 ] = "method"          ; default_values[1 ] = "CHIMES" # Type of MD code used by executable
    default_keys[2 ] = "trajectories"    ; default_values[2 ] = []         # List of trajectory files to modify
    default_keys[3 ] = "temperatures"    ; default_values[3 ] = []         # List of temperatures files for each trajectory file
    default_keys[4 ] = "parameters"      ; default_values[4 ] = []       # List of parameter files to use

    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)    
    
    print("Will subtract force, energy, and stress contributions arising from parameters/files at:")

    if not isinstance(args["parameters"],list):    
        args["parameters"] = [args["parameters"]]
        for i in args["parameters"]:
            print("\t",i)       
    else:
        print("\t",args["parameters"])

    print("Will subtract from trajectory file(s):")
    for i in args["trajectories"]:
        print("\t",i)
    print("Will use the following MD driver:(" + args["method"] + ")")
    print('\t',args["md_driver"])

    params = args["parameters"]
    
    print("Saving original forces to files named like:  b-labeled_full.traj_file_idx-X.dat:")
    
    modify_FES.write_full_FES(args["trajectories"])
    
    for i in range(len(params)):
        modify_FES.subtract_off(params[i], args["md_driver"], args["method"], args["trajectories"], args["temperatures"])
        
    modify_FES.clean_up(args["method"])
        
            


def split_amat(amat, bvec, nproc, ppn):

    """ 
    
    Splits an amat into the desired number of A.XXXX.txt files.
    Generates corresponding dim.XXXX.txt files as well.
    
    Takes roughly 30 minutes to split a ~800 Gb amat
    
    Usage: split_amat("A_comb.txt", "b_comb.txt", 8, 36)
               
    """

    infile = amat
    lines  = helpers.wc_l(bvec)
    nfiles = nproc*ppn
    
    # Ensure we always generate n <= nfiles new files
    
    lines_per_file = int(m.ceil(float(lines)/float(nfiles)))

    print("Will write", nfiles, "files with", lines_per_file, "lines per file")

    # Read the file line by line, print chunks to new numbered files

    file_idx = 0
    line_idx = 0
    line_srt = None
    cols     = 0

    #Aname = "A." + str(file_idx).rjust(len(str(nfiles))+1,'0') + ".txt"
    Aname = "A." + str(file_idx).rjust(4,'0') + ".txt"
    Afstream = open(Aname,'w')

    with open(infile) as ifstream:

            for line in ifstream:

                    if line_idx == 0 and file_idx == 0:

                            cols = line
                            cols = len(cols.split())

                            line_srt  = line_idx

                            print("Counted", cols, "columns")

            
                    if line_idx > 0 and line_idx % lines_per_file == 0:
                    
                        if file_idx >= nfiles:
                            print("LOGIC ERROR: Building too many files")
                            exit()
            
                        print("Working on a new file no.", file_idx)
                        
                        # Close the previous A.*.txt file and write the corresponding dim.*.txt file
                        
                        Afstream.close()
                        
                        #Dname = "dim." + str(file_idx).rjust(len(str(nfiles))+1,'0') + ".txt"
                        Dname = "dim." + str(file_idx).rjust(4,'0') + ".txt"
                        Dfstream = open(Dname,'w')
                        Dfstream.write(str(cols) + " " + str(line_srt) + " " + str(line_idx-1) + " " + str(lines) + "\n") 
                        Dfstream.close()              
            
                        # Start up the next A.*.txt file
            
                        file_idx += 1
                        line_srt  = line_idx

                        Aname = "A." + str(file_idx).rjust(4,'0') + ".txt"
                        #Aname = "A." + str(file_idx).rjust(len(str(nfiles))+1,'0') + ".txt"
                        Afstream = open(Aname,'w')
            
            
                    Afstream.write(line)
                    line_idx += 1
            
    if not Afstream.closed:
        Afstream.close()
            
        Dname = "dim." + str(file_idx).rjust(4,'0') + ".txt"
        #Dname = "dim." + str(file_idx).rjust(len(str(nfiles))+1,'0') + ".txt"
        Dfstream = open(Dname,'w')
        Dfstream.write(str(cols) + " " + str(line_srt) + " " + str(line_idx-1) + " " + str(lines) + "\n") 
        Dfstream.close()
        
    return file_idx+1
    
def gen_weights_one(w_method, this_ALC, b_labeled_i, natoms_i):

    """ 
    Generates weights based on user requested method/parameters, current ALC 
    number, labels in b-labeled.txt, and contents of natoms.txt
    
    Usage: gen_weights(w_method, this_ALC, b_labeled_i, natoms_i)

    Methods:
    
    A. w = a0
    
    B. w = a0*this_ALC^a1 # NOTE: treats this_ALC = 0 as this_ALC = 1
    
    C. w = a0*exp(a1*|X|/a2)
    
    D. w = a0*exp(a1[X-a2]/a3)
    
    E. w = n_atoms^a0
    
    F. w = a0*exp(a1[ X/n_atoms-a2]/a3)
    
    Example wXX value: ["C",[a0,a1,a2]]
    
               
    """
    
    weight = 0.0
    

    if w_method[0] == "A":
    
        if len(w_method[1]) != 1:
            print("ERROR: Found weight request with wrong number of parameters:")
            print(w_method)
            exit()
    
        weight =  float(w_method[1][0])
        
    elif w_method[0] == "B":
    
        if len(w_method[1]) != 2:
            print("ERROR: Found weight request with wrong number of parameters:")
            print(w_method)
            exit()
    
        eff_ALC = this_ALC
        if eff_ALC == 0:
            eff_ALC = 1
            
        
        weight =  float(w_method[1][0]) * float(eff_ALC) ** float(w_method[1][1])
        
    elif w_method[0] == "C":
    
        if len(w_method[1]) != 3:
            print("ERROR: Found weight request with wrong number of parameters:")
            print(w_method)
            exit()
    
        weight =  float(w_method[1][0]) * m.exp( float(w_method[1][1]) * abs(float(b_labeled_i)) / float(w_method[1][2]) )        
         
        
    elif w_method[0] == "D":
    
        if len(w_method[1]) != 4:
            print("ERROR: Found weight request with wrong number of parameters:")
            print(w_method)
            exit()
    
        weight =  float(w_method[1][0]) * m.exp( float(w_method[1][1]) * (float(b_labeled_i)-float(w_method[1][2])) / float(w_method[1][3]) )        
        
    
    elif w_method[0] == "E":
    
        if len(w_method[1]) != 1:
            print("ERROR: Found weight request with wrong number of parameters:")
            print(w_method)
            exit()

        weight =  float(natoms_i)**float(w_method[1][0])
	
    elif w_method[0] == "F":
    
        if len(w_method[1]) != 4:
            print("ERROR: Found weight request with wrong number of parameters:")
            print(w_method)
            exit()
    
        weight =  float(w_method[1][0]) * m.exp( float(w_method[1][1]) * (float(b_labeled_i)/float(natoms_i)-float(w_method[1][2])) / float(w_method[1][3]) )        

    else:
        print("ERROR: Unknown weight method!")
        exit()
        
    return weight
        
        
    
def gen_weights(w_method, this_ALC, b_labeled_i, natoms_i):

    """ 
    Generates weights based on *A SET* of  user requested method/parameters, 
    current ALC number, labels in b-labeled.txt, and contents of natoms.txt
    
    Usage: gen_weights(w_method, this_ALC, b_labeled_i, natoms_i)

    Methods:
    
    A. w = a0
    
    B. w = a0*(this_ALC-1)^a1 # NOTE: treats this_ALC = 0 as this_ALC = 1
    
    C. w = a0*exp(a1*|X|/a2)
    
    D. w = a0*exp(a1[X-a2]/a3)
    
    E. w = n_atoms^a0
    
    F. w = a0*exp(a1[ X/n_atoms-a2]/a3)
    
    Example wXX value: [ ["A","B","C"] , [[a0],[a0,a1],[a0,a1,a2]] ]
    
               
    """

    methods = w_method[0] # e.g. ["A","B","C"]
    wparams = w_method[1] # e.g. [ [a0], [a0,a1], [a0,a1,a2] ]
    
    if len(methods) != len(wparams):
    
        print("ERROR: number of requested weighting methods doesn't match ")
        print("       provided number of weighting parameter sets:")
        print(methods)
        print(wparams)
        exit()
    
    weight = 1.0
    
    for i in range(len(methods)):
    
        weight *= gen_weights_one( [methods[i], wparams[i]], this_ALC, b_labeled_i, natoms_i)
        
    return weight


def solve_amat_started(n_hyper_sets=1):
    
    """ 
    
    Checks whether A-mat solve job has started.
    
    Usage: solve_amat_started()
               
    """
    # Added by BL
    #########################
    if (n_hyper_sets > 1):
        os.chdir("GEN_FF-0")
    else:
        os.chdir("GEN_FF")
    #########################
    
    if os.path.isfile("restart.txt"):
        os.chdir("..")    
        return True
    else:
        os.chdir("..")    
        return False


def solve_amat_completed():  

    """ 
    
    Checks whether A-mat solve job has completed.
    
    Usage: amat_solve_completed()
               
    """
    
    os.chdir("GEN_FF")
    
    if (not os.path.isfile("Ax.txt")) or (not os.path.isfile("x.txt")):
        os.chdir("..")    
        return False
    else:
        os.chdir("..")    
        return True

    
def restart_solve_amat(my_ALC, **kwargs):  

    """ 
    
    Restarts (continues) amat solve.
    
    Usage: restart_solve_amat(1, <arguments>)
    
    Notes: Only compatible with DLARS/DLASSO solver
               
    WARNING: This driver does NOT support SPLITFI functionality in fm_setup.in file. A-matrix
             is handled by the driver itself, based on CHIMES_SOLVE_NODES and CHIMES_SOLVE_QUEUE
             (see split_amat function definition)    
    
    WARNING: The DLARS/DLASSO code zero pads for ints of *4 MAXIMUM* digits
    
    WARNING: Currently only writtien with DLASSO support, NOT DLARS!
               
    """

    ################################
    # 0. Set up an argument parser
    ################################
    
    default_keys   = [""]*14
    default_values = [""]*14
    
    # LSQ controls
    
    default_keys[0 ] = "regression_alg"    ; default_values[0 ] =      "lassolars" # Regression algorithm to be used in lsq2
    default_keys[1 ] = "regression_var"    ; default_values[1 ] =      "1.0E-4"    # SVD eps or Lasso alpha
    default_keys[2 ] = "regression_nrm"    ; default_values[2 ] =    "True"        # Normalizes the a-mat by default ... may not give best result
    default_keys[3 ] = "split_files"       ; default_values[3 ] =      False       # !!! UNUSED
    
    # Overall job controls
    
    default_keys[4 ] = "job_name"           ; default_values[4 ] =    "ALC-"+ repr(my_ALC)+"-lsq-2"   # Name for ChIMES lsq job
    default_keys[5 ] = "job_nodes"         ; default_values[5 ] =    "1"                              # Number of nodes for ChIMES lsq job
    default_keys[6 ] = "job_ppn"           ; default_values[6 ] =    "36"                             # Number of processors per node for ChIMES lsq job
    default_keys[7 ] = "job_walltime"      ; default_values[7 ] =    "1"                              # Walltime in hours for ChIMES lsq job
    default_keys[8 ] = "job_queue"         ; default_values[8 ] =    "pdebug"                         # Queue for ChIMES lsq job
    default_keys[9 ] = "job_account"       ; default_values[9 ] =    "pbronze"                        # Account for ChIMES lsq job
    default_keys[10] = "job_executable"    ; default_values[10] =    ""                               # Full path to executable for ChIMES lsq job
    default_keys[11] = "job_system"        ; default_values[11] =    "slurm"                          # slurm or torque       
    default_keys[12] = "job_email"         ; default_values[12] =    True                             # Send slurm emails?
    default_keys[13] = "node_ppn"          ; default_values[13] =    "36"                             # Send slurm emails?
    
    

    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)

    ################################
    # 1. Run checks before setting up job
    ################################
    
    os.chdir("GEN_FF")    

    if not "dlasso" in args["regression_alg"]:
    
        print("ERROR: restart_solve_amat only available for dlasso and dlars")
        exit()
        
    # Assuming the following files are present from the previous run:
    # A_comb.txt
    # b_comb.txt
    # natoms_comb.txt
    # weights_comb.dat
    # dim.txt
    
    
    # Figure out what the restart job was:
     
    prev_restarts = sorted(glob.glob("restart*txt"))
    tmp = prev_restarts[0:-1]


    def numeric_keys(instr):
        return int(instr.split('-')[-1].split('.')[0])
   
    tmp.sort(key=numeric_keys)
    tmp.append(prev_restarts[-1])
    
    prev_restarts = copy.deepcopy(tmp)
    
    print("Found the following dlars/dlasso restart files:", prev_restarts)

    if len(prev_restarts) == 0:
        print("Bad logic in restart_solve_amat...")
        print("prev_restarts list is empty")
        exit()
    
    if prev_restarts[-1] != "restart.txt":
        print("Bad logic in restart_solve_amat...")
        print("last item in prev_restarts should be restart.txt")
        exit()
        
    # Copy restart.txt to a new (original) name
    
    this_restart = "restart-1.txt"
    
    if len(prev_restarts) == 1:
        helpers.run_bash_cmnd("cp restart.txt " + this_restart)
    else:
        this_restart  = "restart-"
        this_restart += repr(int(prev_restarts[-2].split("-")[1].split(".")[0])+1)
        this_restart += ".txt"
    
        helpers.run_bash_cmnd("cp restart.txt " + this_restart)
        
        
    run_no = int(this_restart.split("-")[1].split(".")[0])

    helpers.run_bash_cmnd("mkdir run-"+repr(run_no))
    helpers.run_bash_cmnd("cp restart.txt dlars.log traj.txt run-"+repr(run_no))

    # Determine whether this was a job with a split amat, and if so, ensure files are correct
    
    do_split = False

    if helpers.wc_l("b_comb.txt") >= (int(args["job_nodes"]) * int(args["job_ppn"]) ):

        do_split = True

        print("Expecting a split A-matrix for faster solve")
        
        n_split_amat = len(glob.glob("A.*.txt"))
        n_split_dims = len(glob.glob("dim.*.txt"))
        n_tot_procs  = int(args["job_nodes"])*int(args["job_ppn"])
        
        if n_split_amat != n_split_dims:
            print("ERROR: Mismatched number of A.XXXX.txt and dim.XXXX.txt files:", n_split_amat, n_split_dims)
            exit()
            
        if n_split_amat > n_tot_procs:
            print("ERROR: Found more A.XXXX.txt files than available procs:", n_split_amat, n_tot_procs)
            exit() 
        
        print("Found", n_split_amat, "A.XXXX.txt file - will run on as many procs.")
        
        if False: # Previous method
        
            n_expected   = int(args["job_nodes"])*int(args["job_ppn"])

            if n_split_amat != n_expected:
                print("ERROR: Expected",n_expected, "A.XXXX.txt files, counted", n_split_amat)
                exit()
        
            if n_split_dims != n_expected:
                print("ERROR: Expected",n_expected, "dim.XXXX.txt files, counted", n_split_dims)
                exit()        
        
        
    ################################
    # 3. Run the actual fit
    ################################
    
    # Create the task string
            
    job_task = args["job_executable"]
    
    if ("dlasso" in args["regression_alg"]) and do_split:
        job_task += " --A A.txt "
    else:
        job_task += " --A A_comb.txt "
        
    job_task += " --b b_comb.txt --weights weights_comb.dat --algorithm " + args["regression_alg"]  + " "
    
    if "dlasso" in args["regression_alg"]:
        job_task += "--active True " 
        job_task += "--alpha " + str(args["regression_var"])  + " "    
        job_task += "--normalize " + str(args["regression_nrm"]) + " "
        job_task += "--nodes "  + str(args["job_nodes"]) + " " 
        job_task += "--cores "  + str(n_split_amat) + " " 
        
        if do_split:
            job_task += "--split_files True    "
        
        
    job_task += "--restart_dlasso_dlars "  + this_restart + " "             
    

    # Launch the job
     
    job_task += " | tee params.txt "

    run_py_jobid = helpers.create_and_launch_job(
        job_name       =     args["job_name"    ] ,
        job_email      =     args["job_email"   ] ,    
        job_nodes      = str(args["job_nodes"    ]),
        job_ppn        = str(args["node_ppn"    ]),
        job_walltime   = str(args["job_walltime"]),
        job_queue      =     args["job_queue"    ] ,
        job_account    =     args["job_account" ] ,
        job_executable =     job_task,
        job_system     =     args["job_system"  ] ,
        job_file       =     "run_lsqpy.cmd")

    os.chdir("..")
    
    return run_py_jobid.split()[0]
    
def parse_hyper_params(**kwargs):

    """
    
    Post-process x.txt file from a fit with multiple unique fm_setup.in files that culminated in an A-matrix that was "pasted" from the A-matrix from each unique fm_setup.in
    Result is a params.txt for each fm_setup.in


    """
    print("Parsing files ...")
    ################################
    # 0. Set up an argument parser
    ################################
    
    default_keys   = [""]*2
    default_values = [""]*2
    
    # Paths
    
    default_keys[0] = "n_hyper_sets"      ; default_values[0] =     1   # Number of unique fm_setup.in files; allows fitting, e.g., multiple overlapping models to the same data
    default_keys[1] = "job_executable"    ; default_values[1] =     ""  # Full path to executable for ChIMES lsq job

    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)    
    
    import numpy as np
    
    # Read in all the raw parameters
    
    x = helpers.cat_to_var("GEN_FF/x.txt")
    
    # Determine how many parameters are associated with each GEN_FF-* folder
    
    dim  = []
    npar = 0
    
    for i in range(int(args["n_hyper_sets"])):
    
        dim.append(int(helpers.head("GEN_FF-" + str(i) + "/dim.txt")[0].split()[0]))
        
    
    # Read GEN_FF-(i)/A.txt matrix
        A = np.loadtxt("GEN_FF-" + str(i) + "/A.txt")
        A = np.array(A, dtype=float)
        A = A.astype('float64')
    
    # Reshape x to a matrix
        x_numeric = np.array(x[npar:npar+dim[i]], dtype=float)
        x_matrix = np.reshape(x[npar:npar+dim[i]], (dim[i], 1))
        x_matrix = x_matrix.astype('float64')
    
    # Perform matrix multiplication
        result_matrix = np.dot(A, x_matrix)
    
    # Save the result_matrix to a file
        np.savetxt("GEN_FF-" + str(i) + "/force.txt", result_matrix)
        np.savetxt("GEN_FF-" + str(i) + "/Ax.txt", result_matrix)
        np.savetxt("GEN_FF-" + str(i) + "/x.txt", x_matrix)
    
        npar += dim[i]

    # Convert x.txt to a real params.txt file
        os.chdir("GEN_FF-" + str(i))
        print("...Generating param.txt file for GEN_FF-" + str(i))
        job_task = args["job_executable"] + "  --algorithm=dlasso --read_output True  " + " > params.txt "
        exit_code = os.system(job_task)
	# Check the exit code to see if the command ran successfully
        if exit_code == 0:
            print("Command executed successfully")
        else:
            print("Command failed with exit code:", exit_code)
        os.chdir("..")


def build_amat(my_ALC, **kwargs):  

    """ 
    
    Generates the A- and b-matrices for an input trajectory.
    
    Usage: build_amat(1, <arguments>)
    
    Notes: See function definition in helpers.py for a full list of options. 
           Requrires config.CHIMES_LSQ.
           Expects to be called from ALC-my_ALC's base folder.
           Returns a job_id for the submitted job.
           
    WARNING: This driver does NOT support SPLITFI functionality in fm_setup.in file. A-matrix
             is handled by the driver itself, based on CHIMES_SOLVE_NODES and CHIMES_SOLVE_QUEUE
             (see split_amat function definition)    
         
    WARNING: DLARS support not yet implemented (DLASSO is available)
               
    """

    ################################
    # 0. Set up an argument parser
    ################################
    
    default_keys   = [""]*27
    default_values = [""]*27
    
    # Paths
    
    default_keys[0 ] = "prev_gen_path"     ; default_values[0 ] =     "../ALC-" + repr(my_ALC-1) + "/GEN_FF/"    # Path to previous ALCs GEN_FF folder -- absolute is best
    default_keys[1 ] = "prev_qm_all_path"  ; default_values[1 ] =     ""                     # Path to previous ALCs <QM>-all folder -- absolute is best
    default_keys[2 ] = "prev_qm_20_path"   ; default_values[2 ] =     ""                     # Path to previous ALCs <QM>-20 folder --absolute is best
    default_keys[3 ] = "do_cluster"        ; default_values[3 ] =     True                   # Should cluser configurations be considered 
    default_keys[4 ] = "split_files"       ; default_values[4 ] =     False                  # !!! UNUSED
    default_keys[5 ] = "include_stress"    ; default_values[5 ] =     False                  # Should stress tensors be included in the A-matrix?
    default_keys[6 ] = "stress_style"      ; default_values[6 ] =     "DIAG"                 # Should the full stress tensor or only diagonal componets be considered? Only used if include_stress is true
    default_keys[7 ] = "do_hierarch"       ; default_values[7 ] =     False                  # Are we building parameters hierarchically?
    default_keys[8 ] = "hierarch_method"   ; default_values[7 ] =     "CHIMES"  	     # Method for determining hierarch. contributions
    default_keys[9 ] = "hierarch_files"    ; default_values[8 ] =     []		     # List of existing parameter files for hierarchical fitting
    default_keys[10] = "hierarch_exe"	   ; default_values[9 ] =     None		     # Executable for subtracting parameter file contributions
    default_keys[11] = "do_correction"     ; default_values[10] =     False		     # Are we fitting a correction to an underlying method?
    default_keys[12] = "correction_exe"    ; default_values[11] =     None		     # Exectuable to evaluate interactions via method to be corrected
    default_keys[13] = "correction_files"  ; default_values[12] =     None                   # Path to directory containng files needed for calculating interactions via method to be corrected
    default_keys[14] = "correction_exe"    ; default_values[13] =     None                   # Executable for method being corrected
    default_keys[15] = "correction_temps"  ; default_values[14] =     None                   # How to handle electron temperatures for 1st ALC
    default_keys[16] = "n_hyper_sets"      ; default_values[15] =     1                      # Number of unique fm_setup.in files; allows fitting, e.g., multiple overlapping models to the same data
    
    
        
    # Job controls
    
    default_keys[17] = "job_name"	   ; default_values[16] =     "ALC-"+ repr(my_ALC)+"-lsq-1"   # Name for ChIMES lsq job
    default_keys[18] = "job_nodes"	   ; default_values[17] =     "2"			      # Number of nodes for ChIMES lsq job
    default_keys[19] = "job_ppn"	   ; default_values[18] =     "36"			      # Number of processors per node for ChIMES lsq job
    default_keys[20] = "job_walltime"	   ; default_values[19] =     "1"			      # Walltime in hours for ChIMES lsq job
    default_keys[21] = "job_queue"	   ; default_values[20] =     "pdebug"  		      # Queue for ChIMES lsq job
    default_keys[22] = "job_account"	   ; default_values[21] =     "pbronze" 		      # Account for ChIMES lsq job
    default_keys[23] = "job_executable"    ; default_values[22] =     ""			      # Full path to executable for ChIMES lsq job
    default_keys[24] = "job_system"	   ; default_values[23] =     "slurm"			      # slurm or torque    
    default_keys[25] = "job_email"	   ; default_values[24] =      True			      # Send slurm emails?
    default_keys[26] = "job_modules"       ; default_values[25] =     ""                              # Modules for the job

    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)
    
    ################################
    # 1. Create the GEN_FF directory(s)
    ################################
    
    
    if int(args["n_hyper_sets"]) == 1:
    
        helpers.run_bash_cmnd("rm -rf GEN_FF")
        helpers.run_bash_cmnd("mkdir  GEN_FF")
        
    else:
    
        for i in range(int(args["n_hyper_sets"])):
        
            helpers.run_bash_cmnd("rm -rf GEN_FF-" + str(i))
            helpers.run_bash_cmnd("mkdir  GEN_FF-" + str(i))       
    
    ################################
    # 2. grab the fm.in and trajlist.in previous iteration, update the contents
    ################################
    
    nfiles      = 0
    nframes_all = 0
    nframes_20  = 0  
    
    lsq_jobs = []
       
    for i in range(int(args["n_hyper_sets"])):
        
        current_iter = i    #Used to save current iteration for hyper sets for other part of the function
   
        GEN_FF   = "GEN_FF"
        FM_SETUP = "fm_setup.in"
       
        if int(args["n_hyper_sets"]) > 1:
       
            GEN_FF  += "-" + str(i)
            FM_SETUP = str(i) + "." + FM_SETUP      
   
    
        if (my_ALC == 0) or ((my_ALC == 1) and (not args["do_cluster"])):
            
            helpers.run_bash_cmnd("cp " + args["prev_gen_path"] + "/" + FM_SETUP   + " " + GEN_FF + "/fm_setup.in")
            helpers.run_bash_cmnd("cp " + args["prev_gen_path"] + "/traj_list.dat" + " " + GEN_FF + "/traj_list.dat")
            
            if len(glob.glob(args["prev_gen_path"] + "/*xyzf"  )) > 0:
                helpers.run_bash_cmnd("cp " + ' '.join(glob.glob(args["prev_gen_path"] + "/*xyzf"  )) + " " + GEN_FF + "/")
            else:
                print("FYI: No .xyzf files to copy from basefiles to " + GEN_FF)
            
            if len(glob.glob(args["prev_gen_path"] + "/*temps")) > 0:
                if (args["do_correction"] and args["correction_temps"]) or (args["do_hierarch"]):
                    helpers.run_bash_cmnd("cp " + ' '.join(glob.glob(args["prev_gen_path"] + "/*temps"  )) + " " + GEN_FF + "/")
 
            nfiles = int(helpers.head(GEN_FF + "/traj_list.dat",1)[0])
    
            # Generate the temperature files
            
            if not args["correction_temps"]:
            
                file_list = helpers.head(GEN_FF + "/traj_list.dat",nfiles+1)[1:]
            
                for i in range(nfiles):
            
                    line = file_list[i].split()
            
                    tmp_frames = int(line[0])
                    tmp_file   =     line[1]
                    
                    if args["do_correction"]:
                        tmp_temp   =     line[2]
            
                        ofstream = open(GEN_FF + "/" + '.'.join(tmp_file.split(".")[0:-1])+".temps",'w')
            
                        for j in range(tmp_frames):
                            ofstream.write(tmp_temp + '\n')
                        ofstream.close()    
    
        else:
            helpers.run_bash_cmnd("cp " + args["prev_gen_path"] + "/" + FM_SETUP + " " + GEN_FF + "/fm_setup.in")
            helpers.run_bash_cmnd("cp " + args["prev_gen_path"] + "/traj_list.dat" + " " + GEN_FF + "/traj_list.dat")
    
            # Get the number of files and number of frames in each file
    
            if args["prev_qm_all_path"] and args["do_cluster"]:
                if current_iter == 0:
                    nfiles     += 1
                    nframes_all = helpers.count_xyzframes_general(args["prev_qm_all_path"] + "/OUTCAR.xyzf")
                else:
                    nfiles = nfiles
                    nframes_all = helpers.count_xyzframes_general(args["prev_qm_all_path"] + "/OUTCAR.xyzf")
                    
            if args["prev_qm_20_path"]:
                if current_iter == 0:
                    nfiles     += 1
                    nframes_20 = helpers.count_xyzframes_general(args["prev_qm_20_path"] + "/OUTCAR.xyzf")
                else:
                    nfiles = nfiles
                    nframes_20 = helpers.count_xyzframes_general(args["prev_qm_20_path"] + "/OUTCAR.xyzf")

                
            # Update the fm_setup.in file
    
    
            ifstream = open(GEN_FF + "/fm_setup.in",'r')
            runfile  = ifstream.readlines()
    
            ofstream = open("tmp",'w')    
    
            found1 = False
            found2 = False
            found3 = False
    
            for i in range(len(runfile)):
    
                if found1:
                    ofstream.write('\t' + "MULTI traj_list.dat" + '\n')
                    found1 = False
                    
                elif found2:
                    ofstream.write('\t' + str(nframes_20+nframes_all) + '\n')
                    found2 = False
                        
                elif found3:
                
                    if args["include_stress"]:
                        if  args["stress_style"] == "DIAG":
                            
                            print("Warning: Fitting first",nframes_20,"diagonal stress tensor components for ALC >",my_ALC)
                            
                            ofstream.write('\t' + "FIRST "    +repr(nframes_20) +'\n')
                            
                            
                        elif args["stress_style"] == "ALL":
                        
                            print("Warning: Fitting first",nframes_20,"total stress tensor components for ALC >",my_ALC)
                        
                            ofstream.write('\t' + "FIRSTALL " +repr(nframes_20) +'\n')
                        else:
                            print("ERROR: Unknown stress style:",args["stress_style"])
                            print("       Options are \"DIAG\" or \"ALL\"")
                            print("Exiting.")
                            
                            exit()
    
                    else:
                        print("Warning: Setting FITSTRS false for ALC >",my_ALC)
                        ofstream.write('\t' + "false" + '\n')
            
                    found3 = False    
                else:
    
                    ofstream.write(runfile[i])
    
                    if "TRJFILE" in runfile[i]:
                        found1 = True
                        
                    if "NFRAMES" in runfile[i]:
                        found2 = True    
                        
                    if "FITSTRS" in runfile[i]:
                        found3 = True            
                    
            ofstream.close()
            ifstream.close()
                            
            helpers.run_bash_cmnd("mv tmp " + GEN_FF + "/fm_setup.in")                

    
            # Update the traj_list file
            ifstream = open(GEN_FF + "/traj_list.dat",'w')
            ifstream.write(repr(nfiles) + '\n')
            if args["prev_qm_20_path"]:
                ifstream.write(repr(nframes_20)  + " " + args["prev_qm_20_path"]  + "/OUTCAR.xyzf\n")
            if args["prev_qm_all_path"] and args["do_cluster"]:
                ifstream.write(repr(nframes_all) + " " + args["prev_qm_all_path"] + "/OUTCAR.xyzf G_ G_ G_\n")
                
            ifstream.close()
            
        ################################
        # 2a. Pre-processing:
        #     ... If hierarchical building is being used, subtract off contributions from other parameter files
        #     ... If fitting a correction, subtract off contributions from the base method
        ################################
    
        n_traj_files = int(helpers.head(GEN_FF + "/traj_list.dat",1)[-1])
        traj_files   = helpers.head(GEN_FF + "/traj_list.dat",nfiles+1)[1:]
        temper_file  = []

    
        # Get trajectory files
    
        if (my_ALC == 0) or ((my_ALC == 1) and (not args["do_cluster"])):
            for i in range(n_traj_files):
                if traj_files[i].split()[1][0] != "/":
                    traj_files[i] = GEN_FF + "/" + traj_files[i].split()[1]
                else:
                    traj_files[i] = traj_files[i].split()[1]
        else:
            for i in range(n_traj_files):
                if i < len(traj_files):
                    traj_files[i] = traj_files[i].split()[1]
                else:
                    print(f"Index {i} is out of range for traj_files")
                
                
        for i in range(n_traj_files):
            if i < len(traj_files):
                temper_file.append(  '.'.join(traj_files[i].split(".")[0:-1]) + ".temps")
            else:
                    print(f"Index {i} is out of range for traj_files")
            
        ################################
        # Hierarch
        ################################

        if args["do_hierarch"]:
    
            subtract(
                md_driver    = args["hierarch_exe"],
                method       = args["hierarch_method"],
                trajectories = traj_files,
                temperatures = temper_file,
                parameters   = args["hierarch_files"])
    
        ################################
        # Correction
        ################################
    
        if args["do_correction"]:
            
            subtract(
                md_driver    = args["correction_exe"],
                method       = args["correction_method"],
                trajectories = traj_files,
                temperatures = temper_file,
                parameters   = args["correction_files"])
            
        ################################
        # 3. Set up and submit the .cmd file for the job
        ################################
    
        os.chdir(GEN_FF)   

      
    
        # Create the task string
        print("Starting job: " + GEN_FF) # Added by BL
        # job_task = "-n " + repr(int(args["job_nodes"])*int(args["job_ppn"])) + " " + args["job_executable"] + " fm_setup.in | tee fm_setup.log"
        

        job_task = args["job_executable"] + " fm_setup.in | tee fm_setup.log"
        if int(args["n_hyper_sets"]) == 1:
            job_task = "-n " + repr(int(args["job_nodes"])*int(args["job_ppn"])) + " " + job_task
        if (args["job_system"] == "slurm" or args["job_system"] == "UM-ARC") and int(args["n_hyper_sets"]) == 1:
            job_task = "srun "   + job_task
        elif args["job_system"] == "TACC" and int(args["n_hyper_sets"]) == 1:
            job_task = "ibrun "   + job_task
        elif int(args["n_hyper_sets"]) == 1:
            job_task = "mpirun " + job_task    
    
        # Launch the job
    
        lsq_jobid_1 = helpers.create_and_launch_job(
            job_name       =      args["job_name"     ] ,
            job_email      =     args["job_email"    ] ,
            job_nodes      =  str(args["job_nodes"   ]),
            job_ppn        =  str(args["job_ppn"     ]),
            job_walltime   =  str(args["job_walltime"]),
            job_queue      =      args["job_queue"   ] ,
            job_account    =      args["job_account" ] ,
            job_executable =      job_task,
            job_modules    =      args["job_modules"],
            job_system     =      args["job_system"  ] ,
            job_file       = "run_chimeslsq.cmd")
    
        lsq_jobs.append(lsq_jobid_1.split()[0])
        
        os.chdir("..")

    return lsq_jobs
    

def solve_amat(my_ALC, **kwargs):  

    """ 
    
    Generates parameters based on generated A- and b-matrices.
    
    Usage: solve_amat(1, <arguments>)
    
    Notes: See function definition in helpers.py for a full list of options. 
           Requrires config.CHIMES_SOLVER.
           Currently only supports lassolars and svd.
           Returns a job_id for the submitted job.
           Assumes last ALC's GEN_FF folder can be accessed from current 
           ALC's base folder via ../ALC-(n-1)/GEN_FF.
               
    WARNING: This driver does NOT support SPLITFI functionality in fm_setup.in file. A-matrix
             is handled by the driver itself, based on CHIMES_SOLVE_NODES and CHIMES_SOLVE_QUEUE
             (see split_amat function definition)        
    
    WARNING: The DLARS/DLASSO code zero pads for ints of *4 MAXIMUM* digits
    
    WARNING: Currently only writtien with DLASSO support, NOT DLARS!
               
    """

    ################################
    # 0. Set up an argument parser
    ################################
    
    default_keys   = [""]*24
    default_values = [""]*24
    
    # Weights
    
    default_keys[21] = "weights_set_alc_0" ; default_values[21] =     False   # Weights to be added to per-atom forces
    default_keys[22] = "weights_alc_0"     ; default_values[22] =     None    # Weights to be added to per-atom forces for clusters  
    
    default_keys[0 ] = "weights_force"     ; default_values[0 ] =     "1.0"   # Weights to be added to per-atom forces
    default_keys[1 ] = "weights_force_gas" ; default_values[1 ] =     "5.0"   # Weights to be added to per-atom forces for clusters  
    default_keys[2 ] = "weights_energy"    ; default_values[2 ] =     "0.1"   # Weights to be added to per-frame energies
    default_keys[3 ] = "weights_energy_gas"; default_values[3 ] =     "0.01"  # Weights to be added to per cluster energies
    default_keys[4 ] = "weights_stress"    ; default_values[4 ] =     "250.0" # Weights to be added to stress tensor components
    default_keys[5 ] = "do_cluster"        ; default_values[5 ] =     True    # Should cluser configurations be considered 
    
    # LSQ controls
    
    default_keys[6 ] = "regression_alg"    ; default_values[6 ] =     "lassolars" # Regression algorithm to be used in lsq2
    default_keys[7 ] = "regression_var"    ; default_values[7 ] =     "1.0E-4"    # SVD eps or Lasso alpha
    default_keys[8 ] = "regression_nrm"    ; default_values[8 ] =     "True"      # Normalizes the a-mat by default ... may not give best result
    default_keys[9 ] = "split_files"       ; default_values[9 ] =     False       # !!! UNUSED
    default_keys[23] = "n_hyper_sets"      ; default_values[23] =     1                      # Number of unique fm_setup.in files; allows fitting, e.g., multiple overlapping models to the same data
    
    
    # Overall job controls
    
    default_keys[10] = "job_name"          ; default_values[10] =     "ALC-"+ repr(my_ALC)+"-lsq-2"        # Name for ChIMES lsq job
    default_keys[11] = "job_nodes"         ; default_values[11] =     "1"                     # Number of nodes for ChIMES lsq job
    default_keys[12] = "job_ppn"           ; default_values[12] =     "36"                    # Number of processors per node for ChIMES lsq job
    default_keys[13] = "job_walltime"      ; default_values[13] =     "1"                     # Walltime in hours for ChIMES lsq job
    default_keys[14] = "job_queue"         ; default_values[14] =     "pdebug"                # Queue for ChIMES lsq job
    default_keys[15] = "job_account"       ; default_values[15] =     "pbronze"               # Account for ChIMES lsq job
    default_keys[16] = "job_executable"    ; default_values[16] =     ""                      # Full path to executable for ChIMES lsq job
    default_keys[17] = "job_system"        ; default_values[17] =     "slurm"                 # slurm or torque    
    default_keys[18] = "job_email"         ; default_values[18] =     True                    # Send slurm emails?
    default_keys[19] = "node_ppn"          ; default_values[19] =     "36"                    # The actual number of procs per node
    default_keys[20] = "job_modules"       ; default_values[20] =     ""                      # Modules for job
    

    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)

    ################################
    # 1. Generate weights for the current ALC's trajectory
    ################################
    
    if int(args["n_hyper_sets"]) > 1:
        if os.path.exists("GEN_FF"):
            helpers.run_bash_cmnd("rm -r " + " GEN_FF")# Remove the existing GEN_FF directory
        os.mkdir("GEN_FF")  # Create the GEN_FF directory

    # Copy common files from GEN_FF-0 and GEN_FF-1 to GEN_FF
        helpers.run_bash_cmnd("cp " + " GEN_FF-0/A.txt" + " GEN_FF")
        helpers.run_bash_cmnd("cp " + " GEN_FF-0/b.txt" + " GEN_FF")
        helpers.run_bash_cmnd("cp " + " GEN_FF-0/b-labeled.txt" + " GEN_FF")
        helpers.run_bash_cmnd("cp " + " GEN_FF-0/natoms.txt" + " GEN_FF")
        helpers.run_bash_cmnd("cp " + " GEN_FF-0/traj_list.dat" + " GEN_FF")
        helpers.run_bash_cmnd("cp " + " GEN_FF-0/fm_setup.in" + " GEN_FF")



        for i in range(1, int(args["n_hyper_sets"])):
            print("Pasting from:", i)
            helpers.run_bash_cmnd("mv " + " GEN_FF/fm_setup.in" + " GEN_FF/0.fm_setup.in")
            helpers.run_bash_cmnd("cp " + f" GEN_FF-{i}/fm_setup.in" + " GEN_FF")
            helpers.run_bash_cmnd("mv " + " GEN_FF/fm_setup.in" + f" GEN_FF/{i}.fm_setup.in")
            paste_cmd = f"paste GEN_FF/A.txt GEN_FF-{i}/A.txt > tmp"
            print(paste_cmd)
            os.system(paste_cmd)
            os.rename("tmp", "GEN_FF/A.txt")               

    os.chdir("GEN_FF")
    helpers.run_bash_cmnd("rm -f weights.dat")
    
    # If the user wants to specify the first ALC's weights, do so. Otherwise, construct them.
    
    user_specified = False 
    
    if (my_ALC == 0) or ((my_ALC == 1) and (not args["do_cluster"])):
        if args["weights_set_alc_0"]:
            helpers.run_bash_cmnd("cp " + args["weights_alc_0"] + " weights.dat")
            user_specified = True
        
    if (not user_specified):
    
        weightfi = open("weights.dat",'w')
    
        ifstream = open("b-labeled.txt",'r')
        contents = ifstream.readlines()
        ifstream .close()
    
        ifstream = open("natoms.txt",'r')
        natoms   = ifstream.readlines()
        ifstream .close()    
    
        for i in range(len(contents)):
    
            tag = contents[i].split()[0]
            val = contents[i].split()[1]
    
            if "+1" in tag:
                if "G_" in tag:
                    weightfi.write(str(gen_weights(args["weights_energy_gas"], my_ALC, val, natoms[i]))+'\n')
                else:
                    weightfi.write(str(gen_weights(args["weights_energy"]    , my_ALC, val, natoms[i]))+'\n')
                    
            elif "s_" in tag:
                weightfi.write(str(gen_weights(args["weights_stress"], my_ALC, val, natoms[i]))+'\n')
            else:
                if "G_" in tag:
                    weightfi.write(str(gen_weights(args["weights_force_gas"], my_ALC, val, natoms[i]))+'\n')
                else:
                    weightfi.write(str(gen_weights(args["weights_force"],     my_ALC, val, natoms[i]))+'\n')
                
        weightfi.close()
    
    os.chdir("..")

    
    ################################
    # 2. Combine current weights, A.txt, and b.txt with previous ALC's
    #    ... Only needed for ALC >= 1
    ################################
    

    if (my_ALC == 0) or ((my_ALC == 1) and (not args["do_cluster"])):
    
        os.chdir("GEN_FF")
        
        if not os.path.isfile("A_comb.txt"): # for restarted jobs that died at this stage
            helpers.run_bash_cmnd("mv A.txt         A_comb.txt"        )
            helpers.run_bash_cmnd("mv b.txt         b_comb.txt"        ) 
            helpers.run_bash_cmnd("mv b-labeled.txt b-labeled_comb.txt")  
            helpers.run_bash_cmnd("mv natoms.txt    natoms_comb.txt"   )
            helpers.run_bash_cmnd("mv weights.dat   weights_comb.dat"  )


    
    else: # "*_comb" files should always exist, because we create them for ALC-0 too
    
        # A-files
    
        #prevfile    = "../ALC-" + `my_ALC-1` + "/GEN_FF/A_comb.txt"
    
        helpers.cat_specific("GEN_FF/A_comb.txt",        ["../ALC-" + repr(my_ALC-1) + "/GEN_FF/A_comb.txt",        "GEN_FF/A.txt"]         )
    
        helpers.cat_specific("GEN_FF/b_comb.txt",        ["../ALC-" + repr(my_ALC-1) + "/GEN_FF/b_comb.txt",        "GEN_FF/b.txt"]         )

        helpers.cat_specific("GEN_FF/b-labeled_comb.txt",["../ALC-" + repr(my_ALC-1) + "/GEN_FF/b-labeled_comb.txt","GEN_FF/b-labeled.txt"] )
        
        helpers.cat_specific("GEN_FF/natoms_comb.txt",   ["../ALC-" + repr(my_ALC-1) + "/GEN_FF/natoms_comb.txt",   "GEN_FF/natoms.txt"]    )

        helpers.cat_specific("GEN_FF/weights_comb.dat",  ["../ALC-" + repr(my_ALC-1) + "/GEN_FF/weights_comb.dat",  "GEN_FF/weights.dat"]   )

        os.chdir("GEN_FF")

    
    if "dlasso" in args["regression_alg"]:
    
        # If we are using dlars/dlasso, need to create the dim.txt file
    
        nvars = len(helpers.head("A_comb.txt",1)[0].split())
        nline =     helpers.wc_l("b_comb.txt")
    
        ofstream = open("dim.txt",'w')
        ofstream.write(repr(nvars) + " " + repr(nline) + '\n') # no. vars, first line, last line, total possible lines
        ofstream.close() 
    
    # Sanity checks    ... As written, these only make sense when a single A-mat is being read
    
    print("A-mat entries:  ",helpers.run_bash_cmnd("wc -l A_comb.txt"      ).split()[0])
    print("b-mat entries:  ",helpers.run_bash_cmnd("wc -l b_comb.txt"      ).split()[0])
    print("natoms entries: ",helpers.run_bash_cmnd("wc -l natoms_comb.txt" ).split()[0])
    print("weight entries: ",helpers.run_bash_cmnd("wc -l weights_comb.dat").split()[0])
    
    if "dlasso" in args["regression_alg"]:
        
        print("Dim file contents:", helpers.cat_to_var("dim.txt")[0])
        
    
    ################################
    # 3. Decide whether to split the A-mat
    ################################

    do_split = False
    
    if "dlasso" in args["regression_alg"]:

        if helpers.wc_l("b_comb.txt") >= (int(args["job_nodes"]) * int(args["job_ppn"])):
        
            do_split = True
        
            print("Splitting A-matrix for faster solve")
        
            helpers.run_bash_cmnd("rm -f A.*.txt dim.*.txt")

            no_files = split_amat("A_comb.txt", "b_comb.txt", int(args["job_nodes"]), int(args["job_ppn"]))
        
            print("    ...split complete")

        if no_files > int(args["job_nodes"])*int(args["job_ppn"]):
            print("ERROR: Number of split files greater than available procs - code implementation error")
            exit()

    ################################
    # 4. Run the actual fit
    ################################
    
    # Create the task string
            
    job_task = args["job_executable"]
    
    if ("dlasso" in args["regression_alg"]) and do_split:
        job_task += " --A A.txt "
    else:
        job_task += " --A A_comb.txt "
        
    job_task += " --b b_comb.txt --weights weights_comb.dat --algorithm " + args["regression_alg"]  + " "
    
          
    if "dlasso" in args["regression_alg"]:
        job_task += "--active True " 
        job_task += "--alpha " + str(args["regression_var"])  + " "    
        job_task += "--normalize " + str(args["regression_nrm"]) + " "
        job_task += "--nodes "  + str(args["job_nodes"]) + " " 
        job_task += "--cores "  + str(no_files) + " " 

        if args["job_system"] == "TACC":
            job_task += "--mpistyle ibrun "
        else:
            job_task += "--mpistyle srun "
        
        if do_split:
            job_task += "--split_files True    "
    
    elif "svd" in args["regression_alg"]:
        job_task += " --eps "   + str(args["regression_var"])
    elif "lasso" in args["regression_alg"]:
        job_task += " --alpha " + str(args["regression_var"])        
    else:
        print("ERROR: unknown regression algorithm: ", args["regression_alg"])
        exit()
    

    # Launch the job
     
    job_task += " | tee params.txt "

    run_py_jobid = helpers.create_and_launch_job(
        job_name       =     args["job_name"    ] ,
        job_email      =     args["job_email"   ] ,    
        job_nodes      = str(args["job_nodes"   ]),
        job_ppn        = str(args["node_ppn"    ]),
        job_walltime   = str(args["job_walltime"]),
        job_queue      =     args["job_queue"   ] ,
        job_account    =     args["job_account" ] ,
        job_executable =     job_task,
        job_system     =     args["job_system"  ] ,
        job_modules    =      args["job_modules"],
        job_file       =     "run_lsqpy.cmd")

    os.chdir("..")
    
    return run_py_jobid.split()[0]


def split_weights():

    """ 
    
    Splits a weights.dat file for parallel learning.
    
    ...Currently, nothing calls this function...
    
    Expects to find:
    
    weights.dat
    b.*.txt
    
    
    """

    # Read all assigned weights
    
    ifstream = open("weights.dat", "r")
    weights  = ifstream.readlines()
    ifstream.close()
    
    
    # Get the number of lines in each bfile
    
    bfiles = sorted(glob.glob("b.*.txt"))

    for i in range(len(bfiles)):
        
        bfiles[i] = helpers.wc_l(bfiles[i])

    # Break up the weight file to match the bfile
    
    start = 0
    pad   = 4 # 1+len(str(len(bfiles)))
    
    print("len:", len(bfiles))
    
    for i in range(len(bfiles)):
        
        outname  = "weights." + repr(i).rjust(pad,'0') + ".dat"
        ofstream = open(outname,'w')
        
        ofstream.write( "\n".join(str(j) for j in weights[start:(start+bfiles[i])] ) + '\n')
        
        ofstream.close()
        
        start += bfiles[i]

    print("weight entries: ",helpers.run_bash_cmnd("wc -l " + "weights.dat").split()[0])
    print("weight entries: ",helpers.run_bash_cmnd("wc -l " + ' '.join(glob.glob("weights.*.dat"))).split()[0])
    
    exit()

