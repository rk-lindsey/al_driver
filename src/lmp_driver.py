# Global (python) modules

import glob # Warning: glob is unsorted... set my_list = sorted(glob.glob(<str>)) if sorting needed
import os

# Localmodules

import helpers
import lmp_to_xyz

def cleanup_and_setup(*argv, **kwargs):
    
    """ 
    
    Removes LMP-X folders, if they exist in the build_dir.
    
    Usage: cleanup_and_setup(<arguments>)
    
    Notes: See function definition in helpers.py for a full list of options. 
           Expects to be run from ALC-X folder
           Should only be run once per ALC
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

    # LMP specific controls

    default_keys[0 ] = "build_dir"        ; default_values[0 ] = "."

    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)    

    for i in args_targets: # 20 all
    
        if args_this_case == -1:
    
            for i in args_targets: # 20 all

                LMP_dir = args["build_dir"] + "/LMP-" + i
            
                if os.path.isdir(LMP_dir):
            
                    helpers.run_bash_cmnd("rm -rf " + LMP_dir)
                    helpers.run_bash_cmnd("mkdir  " + LMP_dir)
                                
                else:
                    helpers.run_bash_cmnd("mkdir  " + LMP_dir)
                
            return

    for i in args_targets: # 20 all
    
        if (i == "all") and (int(args_this_case) > 0):
            continue    

        LMP_dir = args["build_dir"] + "/LMP-" + i
        
        if os.path.isdir(LMP_dir):
        
            helpers.run_bash_cmnd("rm -rf " + LMP_dir + "/*")

            LMP_dir = args["build_dir"] + "/LMP-" + i + "/CASE-" + repr(args_this_case)

            if os.path.isdir(LMP_dir):
                helpers.run_bash_cmnd("rm -rf " + LMP_dir + "/*")
            else:
                helpers.run_bash_cmnd("mkdir  -p " + LMP_dir)
            
        else:
            helpers.run_bash_cmnd("mkdir -p  " + LMP_dir + "/CASE-" + repr(args_this_case))    
 
def continue_job(*argv, **kwargs):    

    """ 
    
    UNUSED FOR LMP - ASSUMES ALL CALCULATIONS RUN WITHIN ALOTTED TIME!
    
    Checks whether all single point calculations ran, resubmits if needed.
    
    Usage: continue_job(<arguments>)
    
    Notes: See function definition in lmp_driver.py for a full list of options. 
           Returns a SLURM jobid list??
               
    """
  

    return []  
     
def check_convergence(my_ALC, *argv, **kwargs):

    """
    
    UNUSED FOR LMP - THERE ARE NO SCF JOBS!
    
    Checks whether  jobs have completed within their requested SCF steps
    
    Usage: check_convergence(my_ALC, no. cases, cp2k_job_types)
     
    # WARNING: This functionality is not used right now. If the  job
    #          doesn't converge, we will declare the problem "impossible" and ignore it
           
    """
    
    ################################
    # 0. Set up an argument parser
    ################################
    
    ### ...argv
    
    args_from = False

    args_cases   = argv[0]    
    args_targets = argv[1] # ... all ... 20
    
    if len(argv) >= 3:
        args_from    = argv[2] # Called from continue_job?

    ######
    # Generate a list of all LMP jobs that crashed

    loc = helpers.run_bash_cmnd("pwd").strip()
    
    total_failed = 0
    
    prefix = ""
    
    for i in range(len(args_targets)): # 20 all
    
        if args_from: # Logic differs depending on whether called from continue_job (True) or check_convergence (False)
            prefix = "\t... (Convergence check): "    
            os.chdir("../..")

        if not os.path.isdir("LMP-" + args_targets[i]):
    
            print("Skipping LMP-" + args_targets[i])
        
            continue
               
        print(prefix + "Working on:","LMP-" + args_targets[i])
    
        os.chdir("LMP-" + args_targets[i])
        
        # Clear out the "tries" file so we try to achieve convergence one more time

        helpers.run_bash_cmnd("rm -f *.tries")
        
        # Build the list of failed jobs for the current CP2K job type (i.e. "all" or "20")
    
        base_list = []    

        iter_list = range(args_cases)
        
        if args_from:
            iter_list = range(args_cases,args_cases+1,1)
        
        for j in iter_list:
            
                tmp_list = sorted(glob.glob("CASE-" + repr(j) + "/*.log.lammps")) # list of all .cp2k.out files for the current ALC's CP2K-20 or CP2K-all specific t/p case
                
                for k in range(len(tmp_list)):

                    if len(helpers.findinfile("Loop time",tmp_list[k]))  != 1:
                        base_list.append('.'.join(tmp_list[k].split(".")[0:4]))
        
        if len(base_list) > 0:
        
            print("Found",len(base_list),"job(s) without \"Loop time\" line:")
            
            for j in range(len(base_list)):
                print("-",base_list[j])
            print("Declaring the problem impossible - renaming to *.ignored and skipping.")
        
        total_failed += len(base_list)
        
        # Renaiming corresponding .out and .tag files
        
        for j in range(len(base_list)):
            helpers.run_bash_cmnd("mv " + base_list[j] + ".log.lammps "    + base_list[j] + ".ignored")
            helpers.run_bash_cmnd("mv " + base_list[j] + ".xyz  "        + base_list[j] + ".ignored")            


    total_failed = 0
    
    os.chdir(loc)
    
    
    return  total_failed
 
def generate_datafile(inxyz, basedir, smearing):

    """ 
    Converts a .xyz file to a LAMMPS data.in file
    
    Usage: generate_cell_and_crds(data.header, data.footer, xyzfile)
    
    Because the LAMMPS data file format is so flexible, users will have to provide a complete .data file template.
    This function will only replace the coordinates with updated values, keeping everything else the same.
    The function assumes xyz coordinates are the last 3 fields of the data file's "Atoms" lines.

    """

    # Note: Smearing is borrowed from QM methods. Not a smearing parameter but does tell us which template files to grab

    xyzstream      = open(inxyz,'r')
    tmpstream      = open(basedir + "/" + str(smearing) + ".data.in", 'r')
    lmpstream      = open(inxyz + ".data.in", 'w')
    natoms         = int(xyzstream.readline())
    
    line    = ""   # Temporary variable that will hold contents of read line
    crd_idx = 0 # index of line on which coordinate file info starts

    # Read/print whatever is in the header portion of the data file
        
    while "Atoms" not in line:
        
        line     = tmpstream.readline()
        crd_idx += 1
        lmpstream.write(line)

    line     = tmpstream.readline() # Account for empty line between "Atoms" and start of coords
    crd_idx += 1 
    lmpstream.write(line)
    xyzstream.readline()            # Account for box length/comment line at start of xyz file   
    
    # Read and update the "Atoms" section
    
    for i in range(natoms):
        
        line = tmpstream.readline()
        line = line.split()
        line = line[0:-3]
        
        linexyz = xyzstream.readline()
        linexyz = linexyz.split()[1:]
       
        lmpstream.write( ' '.join(line + linexyz) + '\n')
        
    # Read/print whatever in the data file comes after "Atoms"
    
    while True:
        
        line = tmpstream.readline()
        
        if line:
            lmpstream.write(line)
        else:
            break
            
    xyzstream.close()
    tmpstream.close()
    lmpstream.close()

def post_process(*argv, **kwargs):   
    

    """ 
    
    Converts a converts a CP2K output files to .xyzf
    Expects stress and energy to be printed to stdout (cp2k.out)
    Expects forces to be printed to  cp2k_traj.forces
    
    Usage: post_process(<arguments>)
    
    Notes: See function definition in CP2Kplus_driver.py for a full list of options. 
               
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


    # CP2K specific controls
    
    default_keys[0 ] = "units"  ; default_values[0 ] = "REAL"        # What units LAMMPS input/output is expected to be in   

    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)    
    
    ################################

    for i in range(len(args_targets)): # 20 all

        if not os.path.isdir("LMP-" + args_targets[i]):
        
            print("Skipping LMP-" + args_targets[i])
            
            continue

            
        print("Working on:","LMP-" + args_targets[i])
    
        os.chdir("LMP-" + args_targets[i])
    
        helpers.run_bash_cmnd("rm -f OUTCAR.xyzf")
        
        log_list = [] # *.log.lammps files
        trj_list = [] # *.traj.lammpstrj files
        
        for j in range(args_cases):
        
            log_list += sorted(glob.glob("CASE-" + repr(j) + "/*.log.lammps"))
            trj_list += sorted(glob.glob("CASE-" + repr(j) + "/*.traj.lammpstrj"))
            
            if len(log_list) != len(trj_list):
                print("ERROR: In lmp_driver.post_process on case",j)
                print("       Number of .log.lammps files and *\#*.traj.lammpstrj files do not match")
                print("       Something went wrong with LAMMPS calculations...")
                print("       Log files: ",len(log_list))
                for f in range(len(log_list)):
                    print("\t\t\t" + log_list[i])
                print("       Traj files: ",len(trj_list))
                for f in range(len(trj_list)):
                    print("\t\t\t" + trj_list[i])
                
                exit()
                
        for j in range(len(log_list)):

            lmp_to_xyz.lmp_to_xyzf( args["units"], trj_list[j], log_list[j])

            outfile = trj_list[j] + ".xyzf"
            
            if os.path.isfile(outfile):
            
                if os.path.isfile("OUTCAR.xyzf"):
            
                    helpers.cat_specific("tmp.dat", ["OUTCAR.xyzf",  outfile])
                else:
                    helpers.cat_specific("tmp.dat", [outfile])
                
                helpers.run_bash_cmnd("mv tmp.dat OUTCAR.xyzf" )
        
        os.chdir("..")
    
def setup_lmp(my_ALC, *argv, **kwargs):    

    """ 
    
    Sets up and launches LAMMPS single point calculations
    
    Usage: setup_lmp(1, <arguments>)
    
    Notes: See function definition in lmp_driver.py for a full list of options. 
           Expects to be run from the ALC-X folder.
           Expects the "all" file in the ALC-X folder.
           Expects the "20" file in the ALC-X/INDEP_X folder.
           Requries a list of atom types.

           Users should provide the following in the ALL_BASEFILES/QM_BASEFILES directory:
           - A single in.lammps file f
           - A data.in file for each case, named like 1.data.in
        
           Script will automatically update coordinates in the data.in file :  
    
    WARNING: Not intended for use with ChIMES cluster entropy-based active learning scheme
              
    """
    
    ################################
    # 0. Set up an argument parser
    ################################
    
    ### ...argv
    
    args_targets = argv[0] # This is a pointer!
    atm_types    = argv[1]
    my_case      = ""
    
    if len(argv) >= 3:
        my_case = str(argv[2])
    
    # Note: For LAMMPS, the smearing field is simply used to select the correct data file, since
    # input format is so flexible (i.e., making auto construction too restricting)
    
    my_smear = "TRAJ_LIST"
        
    if len(argv) >= 4:
        my_smear = str(argv[3])
    
    
    ### ...kwargs
    
    default_keys   = [""]*14
    default_values = [""]*14


    # LMP specific controls
    
    default_keys[0 ] = "basefile_dir"   ; default_values[0 ] = "../LMP_BASEFILES/" # !!!!! ---> POTCAR, KPOINTS, and INCAR
    default_keys[1 ] = "traj_list"      ; default_values[1 ] = "traj_list.dat"      # Traj_list used in fm_setup.in... last column is target temperatura
    default_keys[2 ] = "modules"        ; default_values[2 ] = ""                # Job module files
    default_keys[3 ] = "first_run"      ; default_values[3 ] = False                # Optional... is this the first run? if so, dont search for "CASE" in the name


    # Overall job controls    
    
    default_keys[4 ] = "job_nodes"     ; default_values[4 ] = "2"                   # Number of nodes for ChIMES md job
    default_keys[5 ] = "job_ppn"       ; default_values[5 ] = "36"                  # Number of processors per node for ChIMES md job
    default_keys[6 ] = "job_walltime"  ; default_values[6 ] = "1"                   # Walltime in hours for ChIMES md job
    default_keys[7 ] = "job_queue"     ; default_values[7 ] = "pdebug"              # Queue for ChIMES md job
    default_keys[8 ] = "job_account"   ; default_values[8 ] = "pbronze"             # Account for ChIMES md job
    default_keys[9 ] = "job_executable"; default_values[9 ] = ""                    # Full path to executable for ChIMES md job
    default_keys[10] = "job_system"    ; default_values[10] = "slurm"               # slurm or torque       
    default_keys[11] = "job_file"      ; default_values[11] = "run.cmd"             # Name of the resulting submit script   
    default_keys[12] = "job_email"     ; default_values[12] = True                  # Send slurm emails?
    default_keys[13] = "job_mem  "     ; default_values[13] = 128                   # GB


    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)    
    
    run_lmp_jobid = []
    
    ################################
    # 1. Set up and launch the cp2k single point calculations
    ################################
        
    for i in range(len(args_targets)): # 20 all
    
        if (args_targets[i] == "all") and (int(my_case) > 0):
            continue    
    
        curr_dir = helpers.run_bash_cmnd("pwd").rstrip() # This should be either CASE-X... (ALC>=1) or ...? (ALC==0)
    
        lmp_dir = "LMP-" + args_targets[i] + "/CASE-" + my_case
        
        helpers.run_bash_cmnd("mkdir -p " + lmp_dir)        
            
        # Set up an launch the job
        
        os.chdir(lmp_dir)
        
        # Prepare for the case where smearing is read from traj_list file
        
        temps = None
        
        if my_smear == "TRAJ_LIST":

            # Need to figure out the possible temperatures ... 
            
            ifstream = ""
            
            try:
                ifstream = open("../../../ALC-0/GEN_FF/" + args["traj_list"], 'r')
            except:
                try:
                    ifstream = open("../../../ALC-1/GEN_FF/" + args["traj_list"], 'r')
                except:
                     ifstream = open("../../../ALC-1/GEN_FF-0/" + args["traj_list"], 'r')
                    
                
            

                

            temps    = ifstream.readlines()[1:]

            for j in range(len(temps)):
                temps[j] = temps[j].split()

            ifstream.close()
        
        if args_targets[i] == "20":
        
            my_md_path = curr_dir + "/CASE-" + str(my_case) + "_INDEP_0/" # ONLY EVER COMES FROM FIRST INDEP " + str(my_indep) + "/"

            my_file = "case_" + str(my_case) + ".indep_0.traj_" + args_targets[i] + "F.xyz"

            helpers.run_bash_cmnd("cp " + my_md_path + "/traj_20F.xyz " + my_file)
            
            atoms  = helpers.head(my_file,1)[0].rstrip()
            frames = helpers.wc_l(my_file  )
            frames = frames / (2+int(atoms))

            helpers.break_apart_xyz(frames, my_file)
            
            helpers.run_bash_cmnd("rm -f " + ' '.join(glob.glob("*FORCES*")))
            
            temp = my_smear

            # Generate the .xyz and cell files files

            target_files = ' '.join(sorted(glob.glob("case_" + str(my_case) + ".indep_0.traj_" + args_targets[i] + "F_#*"))).split()

            for j in target_files:
            
                if my_smear == "TRAJ_LIST":

                    temp = int(temps[int(my_case)][2])
                    
                print("\tOn case",my_case,"configuration",j,"generating LMP .data.in file with template data file index:",temp)

                generate_datafile(j, args["basefile_dir"], temp) 
                
                helpers.run_bash_cmnd("cp " + args["basefile_dir"] + "/" + str(temp) + ".in.lammps in.lammps")
                
                
        else:

            print("ERROR: LAMMPS reference method incompatible with ChIMES cluster-entropy based active learning")
            exit()

        ################################
        # 2. Launch the actual job 
        ################################
    
        # Grab the necessary files
    
        helpers.run_bash_cmnd("cp " + ' '.join(glob.glob(args["basefile_dir"] + "/*")) + " .")
        
        ###
        ### Delete any not for this case  -- take care of this later
        ###
        
        ###
        ### Create the task string
        ###
    
        job_task = []
        job_task.append("module load " + args["modules"] + '\n')

        job_task.append("for j in $(ls *\#*xyz.data.in)         ")
        job_task.append("do                             ")
        job_task.append("    TAG=${j%*.xyz.data.in}     ")      
#        job_task.append("    cp " + str(temp) + ".data.in data.in  ")
        job_task.append("    cp $j data.in  ")
        job_task.append("    CHECK=${TAG}.out.lammps    ")
        job_task.append("    if [ -e ${CHECK} ] ; then  ")  
        job_task.append("        continue               ")
        job_task.append("    fi                         ")
        job_task.append("    prev_tries=\"\"              ")
        job_task.append("    if [ -f ${TAG}.tries ] ; then     ")
        job_task.append("       prev_tries=`wc -l ${TAG}.tries | awk '{print $1}'`")
        job_task.append("       if [ $prev_tries -ge 2 ]; then ")
        job_task.append("            continue                   ")
        job_task.append("        fi                             ")
        job_task.append("    fi                                 ")
        job_task.append("    echo \"Attempt\" >> ${TAG}.tries")
        if args["job_system"] == "TACC":
            job_task.append("    ibrun " + "-n " + repr(int(args["job_nodes"])*int(args["job_ppn"])) + " " + args["job_executable"] + " -i in.lammps > ${TAG}.out.lammps  ")
        else:
            job_task.append("    srun -N " + repr(args["job_nodes" ]) + " -n " + repr(int(args["job_nodes"])*int(args["job_ppn"])) + " " + args["job_executable"] + " -i in.lammps > ${TAG}.out.lammps  ")
        
        job_task.append("    mv log.lammps  ${TAG}.log.lammps ") 
        job_task.append("    mv traj.lammpstrj  ${TAG}.traj.lammpstrj ")   
        job_task.append("done")
        
        this_jobid = helpers.create_and_launch_job(job_task,
            job_name       =          "lmp_spcalcs"  ,
            job_email      =     args["job_email"   ] ,            
            job_nodes      = str(args["job_nodes"   ]),
            job_ppn        = str(args["job_ppn"     ]),
            job_walltime   = str(args["job_walltime"]),
            job_queue      =     args["job_queue"   ] ,
            job_account    =     args["job_account" ] ,
            job_system     =     args["job_system"  ] ,
            job_mem        =     args["job_mem"     ] ,
            job_file       =     "run_lmp.cmd")
            
        run_lmp_jobid.append(this_jobid.split()[0])    

        os.chdir(curr_dir)
    
    return run_lmp_jobid        
