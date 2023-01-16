# Global (python) modules

import glob # Warning: glob is unserted... set my_list = sorted(glob.glob(<str>)) if sorting needed
import os

# Localmodules

import helpers
import process_gaussian


######
# Note: Implementation is based on Gaussian 16
######


def NoneIsInf(val):
    if val is None:
        return float("inf")
    else:
        return val

def cleanup_and_setup(*argv, **kwargs):

    """ 
    
    Removes GAUS-X folders, if they exist in the build_dir.
    
    Usage: cleanup_and_setup(<arguments>)
    
    Notes: See function definition in helpers.py for a full list of options. 
           Expects to be run from ALC-X folder
           Should only be run once per ALC
           For "all" type jobs, will only ever set up a "CASE-0" folder, since
           cluster type jobs are not case-specific
               
    """
    
    ################################
    # 0. Set up an argument parser
    ################################
    
    ### ...argv
    
    args_targets   = argv[0] # This is a pointer!
    args_this_case = -1
    
    if len(argv) == 2:
        args_this_case = argv[1]

    ### ...kwargs
    
    default_keys   = [""]*1
    default_values = [""]*1

    # Gaussian specific controls

    default_keys[0 ] = "build_dir"        ; default_values[0 ] = "."

    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)    
    
    
    # Sanity checks (Gaussian should not be used for condensed-phase calculations
    
    if len(args_targets) > 1:
        print("ERROR: Gaussian can only be used for gas-phase calculations")
        print("       but the following were requested:", args_targets)
        exit()
    
    if (len(args_targets) == 1) and (args_targets[0] != "all"):
        print("ERROR: Gaussian can only be used for gas-phase calculations")
        print("       but the following was requested:", args_targets)
        exit()    
        
    # Removes the main "GAUS-X" folder and then creates an empty one

    for i in args_targets: # 20 all
    
        if args_this_case == -1:
    
            for i in args_targets: # 20 all

                gaus_dir = args["build_dir"] + "/GAUS-" + i
    
                if os.path.isdir(gaus_dir):
            
                    helpers.run_bash_cmnd("rm -rf " + gaus_dir)
                    helpers.run_bash_cmnd("mkdir  " + gaus_dir)
                                
                else:
                    helpers.run_bash_cmnd("mkdir  " + gaus_dir)
                
            return
            
    # Builds the GAUS-X/CASE-Y folders

    for i in args_targets: # 20 all

        if (i == "all") and (int(args_this_case) > 0):
            continue
            

        gaus_dir = args["build_dir"] + "/GAUS-" + i

        if os.path.isdir(gaus_dir):
        
            helpers.run_bash_cmnd("rm -rf " + gaus_dir + "/*")

            gaus_dir = args["build_dir"] + "/GAUS-" + i + "/CASE-" + repr(args_this_case)

            if os.path.isdir(gaus_dir):
                helpers.run_bash_cmnd("rm -rf " + gaus_dir + "/*")
            else:
                helpers.run_bash_cmnd("mkdir  -p " + gaus_dir)
            
        else:
            helpers.run_bash_cmnd("mkdir -p  " + gaus_dir + "/CASE-" + repr(args_this_case))


def continue_job(*argv, **kwargs):

    """ 
    
    Checks whether all Gaussian single point calculations ran, resubmits if needed.
    
    Usage: continue_job(<arguments>)
    
    Notes: See function definition in gaus_driver.py for a full list of options. 
           Returns a SLURM jobid list??
               
    """
    
    ################################
    # 0. Set up an argument parser
    ################################
    
    ### ...argv
    
    args_targets = argv[0] # This is a pointer!
    
    args_case    = 0
    
    if len(argv) == 2:
        args_case    = argv[1]
    
    ### ...kwargs
    
    default_keys   = [""]*1
    default_values = [""]*1
    
    default_keys[0 ] = "job_system"    ; default_values[0 ] = "slurm"              # slurm or torque       
    
    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)    
    
    
    ################################
    # 1. Check on job status, resubmit if needed
    ################################    
    
    print("")
    print("    Attempting to continue Gaussian jobs for case: ", args_case)
    
    job_list = []
    
    for i in range(len(args_targets)): # 20 all
    
        if (args_targets[i] == "all") and (int(args_case) > 0):
            continue
    
        CASE_PATH = "CASE-" + repr(args_case)
    
        if os.path.isdir("GAUS-" + args_targets[i] + "/" + CASE_PATH):
        
            os.chdir("GAUS-" + args_targets[i] + "/" + CASE_PATH)

            # Count the number of possible jobs
            
            count_com = len(glob.glob("*.com")) 
            
            # Count the number of completed jobs
            
            count_log = len(glob.glob("*.log"))

            print("")
            print("        Counted .com:", count_com)
            print("        Counted .log:", count_log)
            
            
            # If all jobs haven't completed, resubmit
            
            if count_com > count_log:
            
                print("            Resubmitting.")

                if args["job_system"] == "slurm":
                    job_list.append(helpers.run_bash_cmnd("sbatch run_gaus.cmd").split[-1])
                else:    
                    job_list.append(helpers.run_bash_cmnd("qsub run_gaus.cmd").replace('\n', ''))

            else:
                print("            Not resubmitting.")
            
            print("")
            
            os.chdir("../..")
        else:
            print("Cant find directory GAUS-"+ args_targets[i] + "/" + CASE_PATH)
            print(helpers.run_bash_cmnd("pwd"))

    return job_list    

def check_convergence(my_ALC, *argv, **kwargs):

    """
    
    Checks whether Gaussian jobs have completed within their requested SCF steps
    
    Usage: check_convergence(my_ALC, no. cases, Gaussian_job_types)
    
    Notes: Gaussian_job_types can only be ["all"]
     
    # WARNING: This functionality is not used right now. If the Gaussian job
    #          doesn't converge, we will declare the problem "impossible" and ignore it
           
    #WARNING: Deletes .log files, modifies *.com files
    
    """
    
    # These notes are outdated:
    # Developer notes: gaus_driver.continue_job counts *.coms and *.logs.
    # If !=, then simply resubs the .cmd file and lets the .cmd file take care 
    # of the rest of the logic. The .cmd file also looks to see if *.log 
    # existis. If it does, it skips the job. otherwise, updates .com
    #
    # So what this function does is  delete the corresponding .logs, and then 
    # edits all unconverged .coms to have more requested SCF steps ()
    #
    # Once run, should just be able to call gaus_driver.continue_job as normally
    # done in main.py        

    
    ################################
    # 0. Set up an argument parser
    ################################
    
    ### ...argv

    args_cases   = argv[0]    
    args_targets = argv[1] # ... all ... 20


    # Gaussian specific controls
    
    # ...

    # Overall job controls    
    
    # ...
    
    #print helpers.run_bash_cmnd("pwd")
    
    #os.chdir("ALC-" + `my_ALC`)
    
    total_failed = 0
    
    
    return  total_failed

def generate_coms(inxyz, *argv):

    """ 
    
    Converts a .xyz file to a set of Gaussian .com files.
    
    Usage: (my_file./usr/workspace/wsb/rlindsey/AL_Driver_SVN/rlindsey_branch/xyz, ["C","O"], 6500) # , [1,2])
    
    Notes: Will set up 3 jobs for each .xyz file, R/1, U/2, and U/3,
           where R = spin restricted and U = spin unrestricted, 
           and 1, 2, and 3 refer to spin multiplicity
           
    WARNING: GIVE THIS FUNCTION ***UNWRAPPED*** COORDINATES
    ... see"
    test_unwrap/tight.unwrapped.frame.0.cluster.0.xyz
    
    
    WARNING: ONLY DESIGNED FOR HF AND DFT... WILL NEED TO BE UPDATED FOR OTHER METHODS
               
    """
    
    scratch_dir = argv[0]
    method_link = argv[1] # i.e. "B3LYP/6-311* EmpiricalDispersion=GD2
    
    # Read the coordinates/box lengths
    
    ifstream = open(inxyz,'r')
    natoms   = int(helpers.head(inxyz,1)[0])
    coords   = helpers.tail(inxyz,natoms)
    boxls    = helpers.head(inxyz,2)[-1].rstrip()
    
    ifstream.close()
    
    spin_type = ["R.1","U.2","U.3"]
    
    for spin in spin_type:

        job_name = inxyz + "." + spin + ".com"
        chk_name = scratch_dir + "/" + inxyz + "." + spin + ".chk"

        ifstream = open(inxyz,'r')
        ofstream = open(job_name, 'w')

        # Set up the header portion
        
        ofstream.write("%mem=24GB\n")
        ofstream.write("%chk=" + chk_name + "\n")
        ofstream.write("# force " + spin.split('.')[0] + method_link + " nosymm\n")
        ofstream.write("\n")
        ofstream.write(inxyz + " " + str(natoms) + " " + boxls + '\n')
        ofstream.write("\n")
        ofstream.write("0 " + spin.split('.')[1] + '\n')
        
        # Write the coordinate portion

        for i in range(len(coords)):
            ofstream.write(coords[i]) # should already have the '\n'
        ofstream.write('\n')
        
        ofstream.close()


def post_process(*argv, **kwargs):

    """ 
    
    Converts a converts a Gaussian .log file to .xyzf file
    
    Usage: post_process(<arguments>)
    
    Notes: See function definition in gaus_driver.py for a full list of options. 
               
    """
    
    ################################
    # 0. Set up an argument parser
    ################################
    
    ### ...argv

    args_targets    = argv[0] # ... all ... 20
    args_properties = argv[1] # "ENERGY STRESS" ...etc for the post process script
    
    args_cases    = 1
    
    if len(argv) == 3:
        args_cases    = argv[2]    
    
    
    ### ...kwargs
    
    default_keys   = [""]*1
    default_values = [""]*1
    
    # Not needed.. .py postproc file is in ALDriver:  
    
    default_keys[0 ] = "refdatafile"  ; default_values[0 ] = None

    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)    
    
    ################################
    
    
    # Sanity checks (Gaussian should not be used for condensed-phase calculations
    
    if len(args_targets) > 1:
        print("ERROR: Gaussian can only be used for gas-phase calculations")
        print("       but the following were requested:", args_targets)
        exit()
    
    if (len(args_targets) == 1) and (args_targets[0] != "all"):
        print("ERROR: Gaussian can only be used for gas-phase calculations")
        print("       but the following was requested:", args_targets)
        exit()        

    for i in range(len(args_targets)): # 20 all

        if not os.path.isdir("GAUS-" + args_targets[i]):
        
            print("Skipping GAUS-" + args_targets[i])
            
            continue

            
        print("Working on:","GAUS-" + args_targets[i])
    
        os.chdir("GAUS-" + args_targets[i])
        
        # For continuity with rest of code (which was built for use with VASP),
        # will use log-file-related variable/file names = outcar
    
        helpers.run_bash_cmnd("rm -f OUTCAR.xyzf")
        
        # Get the energies for each of the three jobs (and determine if any ran correctly)
        
        outcar_list = []
        
        for j in range(args_cases):
        
            outcar_list += sorted(glob.glob("CASE-" + repr(j) + "/*R.1*.log"))
            
            
        # Get the energies for each of the three jobs (and determine if any ran correctly)
            
        for j in range(len(outcar_list)):
        
            out_path = "/".join(outcar_list[j].split('/')[0:-1])
            out_name =          outcar_list[j].split('/')[-1]
            out_tag  = '.'.join(out_name.split('.')[0:-3])

            
            job_log = [out_path + "/" + out_tag+".R.1.log", out_path + "/" + out_tag+".U.2.log", out_path + "/" + out_tag+".U.3.log"]
            job_com = [out_path + "/" + out_tag+".R.1.com", out_path + "/" + out_tag+".U.2.com", out_path + "/" + out_tag+".U.3.com"]
            job_enr = [0.0, 0.0, 0.0]
            
            any_complete = False

            for k in range(3):
    
                job_enr[k] = process_gaussian.get_final_energy(job_log[k], "HF")
        
                if type(job_enr[k]) == str:
        
                     job_enr[k]= float(job_enr[k])
                    
                     if job_enr[k] <= 0.0:
                        
                         any_complete = True
             
            if not any_complete:
    
                print("Warning: No single job complete (or all have positive energy) for job name", outcar_list[j], "...skipping.")

                continue    

            # Determine which of the completed jobs are stable    
    
            stable = job_enr.index(min(job_enr, key=NoneIsInf))
        
            print("Post-processing file:",stable,job_com[0], "...")
    
            # Generate the corresponding .xyzf file
        
            target   = None
        
            try:
                target   = helpers.head(job_com[0],30)
                target   = target[[i for i, elem in enumerate(target) if "# force" in elem][0]+2].split()
            except:
                print("Something went wrong while post-processing log file for", job_com[0])
                print("This error is likely unrelated to the ALDriver")
                print("Check the corresponding log-files for more info")
                exit()
            
            natoms   = target[1]
            boxlens  = ' '.join(target[2:])
        
            print("Working on:",job_log[stable])
    
            xyzfname = process_gaussian.get_xyzf(job_log[stable], job_com[stable], natoms, boxlens, args["refdatafile"])

            print("\tConfiguration",i,"completed:", job_log[stable])
        
            if xyzfname: # Makes sure string isn't empty

                if os.path.isfile(xyzfname):
            
                    if os.path.isfile("OUTCAR.xyzf"):
            
                        helpers.cat_specific("tmp.dat", ["OUTCAR.xyzf", xyzfname])
                        helpers.appendlines("OUTCAR.temps" ["0.0"])
                    else:
                        helpers.cat_specific("tmp.dat", [xyzfname])
                        helpers.writelines("OUTCAR.temps" ["0.0"])
                        
                    helpers.run_bash_cmnd("mv tmp.dat OUTCAR.xyzf")    

        os.chdir("..")

def setup_gaus(my_ALC, *argv, **kwargs):

    """ 
    
    Sets up and launches Gaussian single point calculations
    
    Usage: setup_gaus(1, <arguments>)
    
    Notes: See function definition in gaus_driver.py for a full list of options. 
           Expects to be run from the ALC-X folder.
           Expects the "all" file in the ALC-X folder.
           Expects the "20" file in the ALC-X/INDEP_X folder.
           Returns a SLURM jobid
    
    
    WARNING:  ENSURE GAUSSIAN ENVIRONMENT VARS ARE SET... I use:
    
        GAUSS_SCRDIR=/usr/tmp/rlindsey/
        GAUSS_EXEDIR=/usr/WS1/compchem/gaussian/g16/
        export GAUSS_SCRDIR GAUSS_EXEDIR
        g16=${GAUSS_EXEDIR}/g16       
    
              
    """
    
    ################################
    # 0. Set up an argument parser
    ################################
    
    ### ...argv
    
    args_targets = argv[0] # This is a pointer!
    my_case      = 0
    
    if len(argv) >= 2:
        my_case = str(argv[2])
    
    
    ### ...kwargs
    
    default_keys   = [""]*17
    default_values = [""]*17

    # Gaussian specific controls
    
    default_keys[0 ] = "scratch_dir" ; default_values[0 ] = ""
    default_keys[1 ] = "method_link" ; default_values[1 ] = "PBEPBE/6-311+g(2d) EmpiricalDispersion=GD2"         # Gaussian Calculation theory level/basis set
    default_keys[2 ] = "tight_crit"  ; default_values[2 ] = "../../../../tight_bond_crit.dat"                # File with tight bonding criteria for clustering
    default_keys[3 ] = "loose_crit"  ; default_values[3 ] = "../../../../loose_bond_crit.dat"                # File with loose bonding criteria for clustering
    default_keys[4 ] = "clu_code"    ; default_values[4 ] = "/p/lscratchrza/rlindsey/RC4B_RAG/11-12-18/new_ts_clu.cpp"    # Clustering code
    default_keys[5 ] = "compilation" ; default_values[5 ] = "g++ -std=c++11 -O3"                             # Command to compile clustering code
    default_keys[6 ] = "first_run"   ; default_values[6 ] = False                                                # Optional... is this the first run? if so, dont search for "CASE" in the name

    # Overall job controls    
    
    default_keys[7 ] = "job_nodes"     ; default_values[7 ] = "2"           # Number of nodes for ChIMES md job
    default_keys[8 ] = "job_ppn"       ; default_values[8 ] = "36"          # Number of processors per node for ChIMES md job
    default_keys[9 ] = "job_walltime"  ; default_values[9 ] = "1"           # Walltime in hours for ChIMES md job
    default_keys[10] = "job_queue"     ; default_values[10] = "pdebug"      # Queue for ChIMES md job
    default_keys[11] = "job_account"   ; default_values[11] = "pbronze"     # Account for ChIMES md job
    default_keys[12] = "job_executable"; default_values[12] = ""            # Full path to executable for ChIMES md job
    default_keys[13] = "job_system"    ; default_values[13] = "slurm"       # slurm or torque       
    default_keys[14] = "job_file"      ; default_values[14] = "run.cmd"    # Name of the resulting submit script   
    default_keys[15] = "job_email"     ; default_values[15] = True          # Send slurm emails?
    default_keys[16] = "job_mem  "     ; default_values[16] = 128                   # GB
    

    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)    
    
    
    run_gaus_jobid = []
    
    ################################
    # 1. Set up and launch the Gaussian single point calculations
    ################################
        
    for i in range(len(args_targets)): # 20 all ... will always just be "all" for gaussian
    
        if (args_targets[i] == "all") and (int(my_case) > 0):
            print(args_targets[i], my_case, "skipping")
            continue
    
        curr_dir = helpers.run_bash_cmnd("pwd").rstrip() # This should be either CASE-X... (ALC>=1) or ...? (ALC==0)

        gaus_dir = "GAUS-" + args_targets[i] + "/CASE-" + my_case
        
        helpers.run_bash_cmnd("mkdir -p " + gaus_dir)    

        # Set up an launch the job -- assumes these will only ever be gas phase molecs from cluster selection
        
        os.chdir(gaus_dir)
        
        ifstream     = open(curr_dir + "/" + args_targets[i] + ".selection.dat", 'r') # all.selection.dat ... a list of indices
        target_files = ifstream.readlines()
        ifstream     .close()
        
        ifstream     = open(curr_dir + "/" + args_targets[i] + ".xyzlist.dat",   'r') # all.xyzlist.dat ... a list of file names
        contents     = ifstream.readlines()
        ifstream     .close()
        
        # Make a temporary directory for unwrapping and prepare the cluster code (See below) 
        
        #helpers.run_bash_cmnd("tmp_unwrap")
        
        helpers.run_bash_cmnd(args["compilation"] + " -o new_ts_clu " + args["clu_code"])

        for j in range(len(target_files)):
            
            # Figure out which files we're trying to submit

            sel_file = contents[int(target_files[j].rstrip())].split()
            sel_file = sel_file[len(sel_file)-1]
            
            case_check = "CASE-" + my_case
            
            if (not args["first_run"]) and (case_check not in sel_file):

                continue
                
            # Unwrap the coordinates for the gaussian job
            
            helpers.run_bash_cmnd("rm -rf tmp_unwrap")
            helpers.run_bash_cmnd("mkdir tmp_unwrap")
            
            # Sel file looks like: (../../) CFG_REPO-2.50gcc_9000K.OUTCAR.25F.xyzf/tight.wrapped.frame.8.cluster.40.xyz
            
            helpers.run_bash_cmnd("cp " + "../../" + sel_file + " tmp_unwrap/tmp.xyz")
            os.chdir("tmp_unwrap")    
            
            helpers.run_bash_cmnd("../new_ts_clu tmp.xyz 1 " + args["tight_crit"])        
            os.chdir("..")
            
            sel_file = sel_file.replace('/','.') 
            sel_file = sel_file + ".unwrap.xyz"
        
            helpers.run_bash_cmnd("cp tmp_unwrap/tight.unwrapped.frame.0.cluster.0.xyz " + sel_file)


            # Build the .com file
            
            generate_coms(sel_file, args["scratch_dir"], args["method_link"])


        ################################
        # 2. Launch the actual job 
        ################################

        # Grab the necessary files
    
        helpers.run_bash_cmnd("cp " + ' '.join(glob.glob(args["basefile_dir"] + "/*")) + " .")
    
        # Create the task string
                
        job_task = []
        #job_task.append("module load " + args["modules"] + '\n')
    
    
        job_task.append("for j in $(ls *.com)            ")    
        job_task.append("do                ")
        job_task.append("    TAG=${j%*.com}            ")    
        job_task.append("    CHECK=${TAG}.log    ")
        job_task.append("    if [ -e ${CHECK} ] ; then ")    
        job_task.append("        continue    ")    
        job_task.append("    fi            ")    
        job_task.append("    timeout 1h " + args["job_executable"] + " -p=" + str(args["job_ppn"]) + " -w=${SLURM_JOB_NODELIST} < ${TAG}.com > log.log")
        job_task.append("    mv log.log ${TAG}.log    ")
        job_task.append("done    ")
    
        this_jobid = helpers.create_and_launch_job(job_task,
            job_name       =          "gaus_spcalcs"  ,
            job_email      =     args["job_email"   ] ,            
            job_nodes      = str(args["job_nodes"    ]),
            job_ppn        = str(args["job_ppn"    ]),
            job_walltime   = str(args["job_walltime"]),
            job_queue      =     args["job_queue"    ] ,
            job_account    =     args["job_account" ] ,
            job_system     =     args["job_system"  ] ,
            job_mem        =     args["job_mem"     ],
            job_file       =     "run_gaus.cmd")
            
        run_gaus_jobid.append(this_jobid.split()[0])    
    
        os.chdir(curr_dir)
    
    return run_gaus_jobid        
