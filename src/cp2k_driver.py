# Global (python) modules

import glob # Warning: glob is unsorted... set my_list = sorted(glob.glob(<str>)) if sorting needed
import os

# Localmodules

import helpers
import cp2k_to_xyz

def cleanup_and_setup(*argv, **kwargs):
    
    """ 
    
    Removes CP2K-X folders, if they exist in the build_dir.ss
    
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

    # CP2K+ specific controls

    default_keys[0 ] = "build_dir"        ; default_values[0 ] = "."

    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)    

    for i in args_targets: # 20 all
    
        if args_this_case == -1:
    
            for i in args_targets: # 20 all

                CP2K_dir = args["build_dir"] + "/CP2K-" + i
            
                if os.path.isdir(CP2K_dir):
            
                    helpers.run_bash_cmnd("rm -rf " + CP2K_dir)
                    helpers.run_bash_cmnd("mkdir  " + CP2K_dir)
                                
                else:
                    helpers.run_bash_cmnd("mkdir  " + CP2K_dir)
                
            return

    for i in args_targets: # 20 all
    
        if (i == "all") and (int(args_this_case) > 0):
            continue    

        CP2K_dir = args["build_dir"] + "/CP2K-" + i
        
        if os.path.isdir(CP2K_dir):
        
            helpers.run_bash_cmnd("rm -rf " + CP2K_dir + "/*")

            CP2K_dir = args["build_dir"] + "/CP2K-" + i + "/CASE-" + repr(args_this_case)

            if os.path.isdir(CP2K_dir):
                helpers.run_bash_cmnd("rm -rf " + CP2K_dir + "/*")
            else:
                helpers.run_bash_cmnd("mkdir  -p " + CP2K_dir)
            
        else:
            helpers.run_bash_cmnd("mkdir -p  " + CP2K_dir + "/CASE-" + repr(args_this_case))    
 
def continue_job(*argv, **kwargs):    

    """ 
    
    Checks whether all CP2K single point calculations ran, resubmits if needed.
    
    Usage: continue_job(<arguments>)
    
    Notes: See function definition in cp2k_driver.py for a full list of options. 
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
    print("    Attempting to continue CP2K jobs for case: ", args_case)
    
    job_list = []
    
    for i in range(len(args_targets)): # 20 all
    
        if (args_targets[i] == "all") and (int(args_case) > 0):
            continue
    
        CASE_PATH = "CASE-" + repr(args_case)
    
        if os.path.isdir("CP2K-" + args_targets[i] + "/" + CASE_PATH):
        
            os.chdir("CP2K-" + args_targets[i] + "/" + CASE_PATH)

            # Count the number of possible jobs
            
            count_xyz    = len(glob.glob("case*.xyz.xyz")) 
            count_forces = len(glob.glob("case*.forces")) 
            
            # Check for convergence issues
            
            ###This has been commented out but should be checked at some point to know why it was here when main also calls it?
            # check_convergence(-1, args_case,args_targets, True) # First arg isn't used
         
            # Count the number of completed jobs
            
            count_out = len(glob.glob("case*.cp2k.out"))

            print("")
            print("        Counted .xyz:   ", count_xyz)
            print("        Counted .forces:", count_forces)
            
            
            # If all jobs haven't completed, resubmit
            
            if count_xyz > count_forces:
            
                print("            Resubmitting.")

                if args["job_system"] == "slurm" or args["job_system"] == "TACC" or args["job_system"] == "UM-ARC":
                    job_list.append(helpers.run_bash_cmnd("sbatch run_cp2k.cmd").split()[-1])
                else:    
                    job_list.append(helpers.run_bash_cmnd("qsub run_cp2k.cmd").replace('\n', ''))

            else:
                print("            Not resubmitting.")
            
            print("")
            
            os.chdir("../..")
        else:
            print("Cant find directory CP2K-"+ args_targets[i] + "/" + CASE_PATH)
            print(helpers.run_bash_cmnd("pwd"))

    return job_list  
     
def check_convergence(my_ALC, *argv, **kwargs):

    """
    
    Checks whether CP2K jobs have completed within their requested SCF steps
    
    Usage: check_convergence(my_ALC, no. cases, cp2k_job_types)
     
    # WARNING: This functionality is not used right now. If the CP2K job
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


    # CP2K specific controls
    
    # ...

    # Overall job controls    
    
    # ...
    
    #print helpers.run_bash_cmnd("pwd")
    
    #os.chdir("ALC-" + `my_ALC`)
    
    # At this point, I'm not sure if CP2K prints anything if convergence not reached within requested SCF steps
    # Also note that CP2K has two SCF loops, inner and outer
    
    
    ######
    # Generate a list of all CP2K jobs that crashed

    loc = helpers.run_bash_cmnd("pwd").strip()
    
    total_failed = 0
    
    prefix = ""
    
    for i in range(len(args_targets)): # 20 all
    
        if args_from: # Logic differs depending on whether called from continue_job (True) or check_convergence (False)
            prefix = "\t... (Convergence check): "    
            os.chdir("../..")

        if not os.path.isdir("CP2K-" + args_targets[i]):
    
            print("Skipping CP2K-" + args_targets[i])
        
            continue
               
        print(prefix + "Working on:","CP2K-" + args_targets[i])
    
        os.chdir("CP2K-" + args_targets[i])
        
        # Clear out the "tries" file so we try to achieve convergence one more time

        # THIS LINE IS COMMENTED OUT AND NEEDS TO BE INVESTIGATED!!!!!
        #####
        # helpers.run_bash_cmnd("rm -f *.tries")
        #####
        # Build the list of failed jobs for the current CP2K job type (i.e. "all" or "20")
    
        base_list = []    

        iter_list = range(args_cases)
        
        if args_from:
            iter_list = range(args_cases,args_cases+1,1)
        
        for j in iter_list:
            
                tmp_list = sorted(glob.glob("CASE-" + repr(j) + "/*.cp2k.out")) # list of all .cp2k.out files for the current ALC's CP2K-20 or CP2K-all specific t/p case
                
                for k in range(len(tmp_list)):

                    if len(helpers.findinfile("SCF run NOT converged",tmp_list[k]))  > 0:
                        base_list.append('.'.join(tmp_list[k].split(".")[0:4]))
        
        if len(base_list) > 0:
        
            print("Found",len(base_list),"job(s) with error SCF \"run NOT converged\":")
            
            for j in range(len(base_list)):
                print("-",base_list[j])
            print("Declaring the problem impossible - renaming to *.ignored and skipping.")
        
        total_failed += len(base_list)
        
        # Renaiming corresponding .out and .xyz files
        
        for j in range(len(base_list)):
            helpers.run_bash_cmnd("mv " + base_list[j] + ".cp2k.out "                 + base_list[j] + ".cp2k.out"           + ".ignored")   
            helpers.run_bash_cmnd("mv " + base_list[j] + ".xyz "                      + base_list[j] + ".xyz"                + ".ignored")   
            helpers.run_bash_cmnd("mv " + base_list[j] + ".cp2k_traj.forces "         + base_list[j] + ".cp2k_traj.forces"   + ".ignored")   



    total_failed = 0
    
    os.chdir(loc)
    
    
    return  total_failed
    
def generate_cell_and_crds(inxyz, *argv): 
    
    
    """ 
    
    Converts a .xyz file to a CP2K .cell and .xyz files
    
    Usage: (my_file./usr/workspace/wsb/rlindsey/AL_Driver_SVN/rlindsey_branch/xyz, ["C","O"], 6500) # , [1,2])
    
    Notes: The second argument is list of atom types
           The final argument is the smearing temperature, in Kelvin
              
    """
    
    atm_types  = argv[0] # pointer!
    smearing   = float(argv[1])
    ifstream   = open(inxyz,'r')
    xyzstream  = open(inxyz + ".xyz", 'w')
    celstream  = open(inxyz + ".cell", 'w')
    
    # Determine number of atoms and box dimensions
        
    box = ifstream.readline()           # No. atoms
    box = ifstream.readline().split()   # Box lengths
        
    a = [0.0]*3
    b = [0.0]*3
    c = [0.0]*3
    
    if box[0] == "NON_ORTHO":
        
        for i in range(3):
            
            a[i] = box[1+i]
            b[i] = box[1+i+3]
            c[i] = box[1+i+6]
    else:
    
        a[0] = box[0]
        b[1] = box[1]
        c[2] = box[2]
    
    # Write box dimensions
    
    celstream.write("A" + " " + ' '.join(map(str,a)) + '\n')
    celstream.write("B" + " " + ' '.join(map(str,b)) + '\n')
    celstream.write("C" + " " + ' '.join(map(str,c)) + '\n')
        
    # Count up the number of atoms of each type
    
    contents = ifstream.readlines()
    contents.sort() # To remain constistent with all other QM methods that expects sorted coordinates
    
    natm_types = [0]*len(atm_types)
    
    for i in range(len(contents)):
    
        for j in range(len(atm_types)):
            
            if atm_types[j] in contents[i]:
                
                natm_types[j] += 1
                
    # Remove any elements that don't appear in the coordinate file
    # But first, make sure everything is sorted 
    
    tmp = list(zip(atm_types,natm_types))
    tmp.sort() # Sorts by the first entry (atom types) ... alphabetical
    
    for i in range(len(tmp)-1,-1,-1): # Goes through list backwards
        
        if tmp[i][1] == 0: 
        
            tmp.pop(i)
    
    atm_types  = list(list(zip(*tmp))[0])
    natm_types = list(map(int,list(list(zip(*tmp))[1])))
    
    # Finish up the header portion
    
    xyzstream.write(str(len(contents)) + "\n")
    xyzstream.write(' '.join(map(str,a)) + " " + ' '.join(map(str,b)) + " " + ' '.join(map(str,c)) + " smearing: " + str(smearing) + " K" "\n")

    for i in range(len(contents)):
        
        line = contents[i].split()                
        line = str(' '.join(line[:])) + '\n'
        xyzstream.write(line)
            
    xyzstream.close()            
    
def post_process(*argv, **kwargs):   
    

    """ 
    
    Converts a CP2K output files to .xyzf
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
    
    default_keys[0 ] = "cp2k_postproc"  ; default_values[0 ] = ""        # Parses a results.tag for E and stress tensor and detailed.out for forces     

    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)    
    
    ################################

    for i in range(len(args_targets)): # 20 all

        if not os.path.isdir("CP2K-" + args_targets[i]):
        
            print("Skipping CP2K-" + args_targets[i])
            
            continue

            
        print("Working on:","CP2K-" + args_targets[i])
    
        os.chdir("CP2K-" + args_targets[i])
    
        helpers.run_bash_cmnd("rm -f OUTCAR.xyzf")
        
        out_list = [] # *.cp2k.out files
        crd_list = [] # *.xyz.xyz files
        frc_list = [] # *cp2k_traj.forces files
        
        for j in range(args_cases):
        
            out_list += sorted(glob.glob("CASE-" + repr(j) + "/*.cp2k.out"))
            crd_list += sorted(glob.glob("CASE-" + repr(j) + "/*.xyz.xyz"))
            frc_list += sorted(glob.glob("CASE-" + repr(j) + "/*.cp2k_traj.forces"))
            
            if len(out_list) != len(crd_list):
                print("ERROR: In cp2k_driver.post_process on case",j)
                print("       Number of .cp2k.out files and *\#*.xyz.xyz files do not match")
                print("       Something went wrong with CP2K calculations...")
                exit()
            if len(out_list) != len(frc_list):
                print("ERROR: In cp2k_driver.post_process on case",j)
                print("       Number of .cp2k.out files and .cp2k_traj.forces files do not match")
                print("       Something went wrong with CP2K calculations...")
                exit()                
                
        for j in range(len(out_list)):

            cp2k_to_xyz.cp2k_to_xyzf(crd_list[j], out_list[j], frc_list[j], args_properties)
            
            outfile = crd_list[j].split(".xyz")
            outfile = ''.join(outfile) + ".xyzf"

            # Figure out the temperature
            
            tmp_temp = helpers.findinfile("MD_PAR| Temperature [K]",out_list[j])[0].split()[-1]

            tmpfile = crd_list[j].split(".xyz")
            tmpfile = ''.join(outfile) + ".temps"
            tmpstream = open(tmpfile,'w')
            tmpstream.write(tmp_temp + '\n')
            tmpstream.close()
            
            ###
            
            if "ENERGY" in args_properties: # Make sure the configuration energy is less than or equal to zero

            
                tmp_ener = float(helpers.findinfile("ENERGY| Total FORCE_EVAL ( QS ) energy [a.u.]: ",out_list[j])[0].split()[-1])
                
                if tmp_ener >= 0.0:
                    
                    print("Warning: CP2K energy is positive energy for job name", resulttg_list[j], ":", tmp_ener, "...skipping.")
                    continue
            
            if os.path.isfile(outfile):
            
                if os.path.isfile("OUTCAR.xyzf"):
            
                    helpers.cat_specific("tmp.dat", ["OUTCAR.xyzf",  outfile])
                    helpers.cat_specific("tmp.tmp", ["OUTCAR.temps", tmpfile])
                else:
                    helpers.cat_specific("tmp.dat", [outfile])
                    helpers.cat_specific("tmp.tmp", [tmpfile])
                
                helpers.run_bash_cmnd("mv tmp.dat OUTCAR.xyzf" )
                helpers.run_bash_cmnd("mv tmp.tmp OUTCAR.temps")
        
        os.chdir("..")
    
def setup_cp2k(my_ALC, *argv, **kwargs):    

    """ 
    
    Sets up and launches CP2K single point calculations
    
    Usage: setup_cp2k(1, <arguments>)
    
    Notes: See function definition in cp2k_driver.py for a full list of options. 
           Expects to be run from the ALC-X folder.
           Expects the "all" file in the ALC-X folder.
           Expects the "20" file in the ALC-X/INDEP_X folder.
           Requries a list of atom types.
           Requires a data_dir location, i.e. to set @SET data_dir /nfs/turbo/coe-rklinds/software/cp2k/data/ in cp2k.in

           Users should provide the following in the ALL_BASEFILES/QM_BASEFILES directory:
           - A cp2k.inp file for each temperature named like 300.cp2k.inp
           - A cp2k.qm_basis-block.inp file for each element named like Si.cp2k.qm_basis-block.inp
           - A cp2k.qm_psuedo-block.inp file
    
           Script will automatically generate other necesssary files:

           - cell_file ald.cell                 # Text file with cell vectors (cp2k format)
           - crds_file ald.xyz                  # XYZ file with system coordinates (xyz format)
           - intg_file cp2k.md_int-block.inp    # MD integrator specification, and energy I/O print frequency
           - mdio_file cp2k.md_io-block.inp     # I/O file names/frequencies for MD (except energy!)

           Returns a SLURM jobid
        
    WARNING: For ALC-0, smearing is taken to be the corresponding temeprature
             in the traj_list.dat file.
    
    WARNING: For ALC-1+, smearing is a specified parameter.    
    
    WARNING: Largely only intended for liquids, so far.    
              
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
    
    my_smear = "TRAJ_LIST"
        
    if len(argv) >= 4:
        my_smear = str(argv[3])
    
    
    ### ...kwargs
    
    default_keys   = [""]*15
    default_values = [""]*15


    # CP2K specific controls
    
    default_keys[0 ] = "basefile_dir"   ; default_values[0 ] = "../CP2K_BASEFILES/" # !!!!! ---> POTCAR, KPOINTS, and INCAR
    default_keys[1 ] = "traj_list"      ; default_values[1 ] = "traj_list.dat"      # Traj_list used in fm_setup.in... last column is target temperatura
    default_keys[2 ] = "modules"        ; default_values[2 ] = "mkl"                # Job module files
    default_keys[3 ] = "data_dir"       ; default_values[3 ] = "."                  # Post_proc_lsq*py file... should also include the python command
    default_keys[4 ] = "first_run"      ; default_values[4 ] = False                # Optional... is this the first run? if so, dont search for "CASE" in the name


    # Overall job controls    
    
    default_keys[5 ] = "job_nodes"     ; default_values[5 ] = "2"                   # Number of nodes for ChIMES md job
    default_keys[6 ] = "job_ppn"       ; default_values[6 ] = "36"                  # Number of processors per node for ChIMES md job
    default_keys[7 ] = "job_walltime"  ; default_values[7 ] = "1"                   # Walltime in hours for ChIMES md job
    default_keys[8 ] = "job_queue"     ; default_values[8 ] = "pdebug"              # Queue for ChIMES md job
    default_keys[9 ] = "job_account"   ; default_values[9 ] = "pbronze"             # Account for ChIMES md job
    default_keys[10] = "job_executable"; default_values[10] = ""                    # Full path to executable for ChIMES md job
    default_keys[11] = "job_system"    ; default_values[11] = "slurm"               # slurm or torque       
    default_keys[12] = "job_file"      ; default_values[12] = "run.cmd"             # Name of the resulting submit script   
    default_keys[13] = "job_email"     ; default_values[13] = True                  # Send slurm emails?
    default_keys[14] = "job_mem  "     ; default_values[14] = 128                   # GB


    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)    
    
    run_cp2k_jobid = []
    
    ################################
    # 1. Set up and launch the cp2k single point calculations
    ################################
        
    for i in range(len(args_targets)): # 20 all
    
        if (args_targets[i] == "all") and (int(my_case) > 0):
            continue    
    
        curr_dir = helpers.run_bash_cmnd("pwd").rstrip() # This should be either CASE-X... (ALC>=1) or ...? (ALC==0)
    
        cp2k_dir = "CP2K-" + args_targets[i] + "/CASE-" + my_case
        
        helpers.run_bash_cmnd("mkdir -p " + cp2k_dir)        
            
        # Set up an launch the job
        
        os.chdir(cp2k_dir)
        
        # Prepare for the case where smearing is read from traj_list file
        
        temps = None
        
        if my_smear == "TRAJ_LIST":

            # Need to figure out the possible temperatures ... 
            
            ifstream = ""
            
            try:
                ifstream = open("../../../ALC-0/GEN_FF/" + args["traj_list"], 'r')
            except:
                ifstream = open("../../../ALC-1/GEN_FF/" + args["traj_list"], 'r')
                

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
                    
                print("\tOn case",my_case,"configuration",j,"generating CP2K .xyz and cell file with smearing temperature:",temp)

                generate_cell_and_crds(j, atm_types, temp)    
                
        else:

            ifstream     = open(curr_dir + "/" + args_targets[i] + ".selection.dat", 'r') # all.selection.dat ... a list of indices
            target_files = ifstream.readlines()
            ifstream     .close()
            
            ifstream     = open(curr_dir + "/" + args_targets[i] + ".xyzlist.dat",   'r') # all.xyzlist.dat ... a list of file names
            contents     = ifstream.readlines()
            ifstream     .close()

            temp = my_smear

            for j in range(len(target_files)):

                sel_file = contents[int(target_files[j].rstrip())].split()
                sel_file = sel_file[len(sel_file)-1]
                
                case_check = "CASE-" + my_case
                
                if (not args["first_run"]) and (case_check not in sel_file):

                    continue

                if my_smear == "TRAJ_LIST":

                    for k in range(len(temps)):
    
                        if ("CASE-" + str(k) in sel_file) or (temps[k][2] in sel_file):
                    
                            temp = temps[k][2]

                            break
                            
                print("\tOn case",my_case,"configuration",sel_file,"generating POSCAR with smearing temperature:",temp)

                generate_cell_and_crds(curr_dir + "/" + sel_file, atm_types, temp)

                helpers.run_bash_cmnd("mv " + curr_dir + "/" + sel_file + ".xyz tmp.xyz")
                helpers.run_bash_cmnd("mv " + curr_dir + "/" + sel_file + ".cell tmp.cell")
                
    
                sel_xyz  = sel_file + ".xyz"
                sel_cell = sel_file + ".cell"
                
                sel_xyz  = sel_xyz .replace('/','.')
                sel_cell = sel_cell.replace('/','.')
                
                helpers.run_bash_cmnd("mv  tmp.xyz  " + sel_xyz)
                helpers.run_bash_cmnd("mv  tmp.cell " + sel_cell)


        ################################
        # 2. NEW: Generate the intg_file and mdio_file files
        ################################
        #   - cell_file ald.cell                 # Text file with cell vectors (cp2k format)
        #   - crds_file ald.xyz                  # XYZ file with system coordinates (xyz format)
        #   - intg_file cp2k.md_int-block.inp    # MD integrator specification, and energy I/O print frequency
        #   - mdio_file cp2k.md_io-block.inp     # I/O file names/frequencies for MD (except energy!)
        
        intg_stream = open("cp2k.md_int-block.inp",'w')    
        intg_stream.write("ENSEMBLE            NVT    \n")
        intg_stream.write("&THERMOSTAT                \n")
        intg_stream.write("    TYPE            NOSE   \n")
        intg_stream.write("    REGION          GLOBAL \n")
        intg_stream.write("    &NOSE                  \n")
        intg_stream.write("        LENGTH      3      \n")
        intg_stream.write("        YOSHIDA     3      \n")
        intg_stream.write("        TIMECON     50.0   \n")
        intg_stream.write("        MTS         2      \n")
        intg_stream.write("    &END NOSE              \n")
        intg_stream.write("&END THERMOSTAT            \n")
        intg_stream.write("&PRINT                     \n")
        intg_stream.write("    &ENERGY                \n")
        intg_stream.write("        FILENAME  md.energy\n")
        intg_stream.write("    &END ENERGY            \n")
        intg_stream.write("&END PRINT                 \n")
        intg_stream.close()
        
        mdio_stream = open("cp2k.md_io-block.inp" ,'w')
        mdio_stream.write("&TRAJECTORY                    \n")
        mdio_stream.write("    FILENAME = cp2k_traj.xyz   \n")
        mdio_stream.write("&END TRAJECTORY                \n")
        mdio_stream.write("&FORCES                        \n")
        mdio_stream.write("    FILENAME = cp2k_traj.forces\n")
        mdio_stream.write("&END FORCES                    \n")
        mdio_stream.write("&CELL                          \n")
        mdio_stream.write("    FILENAME = cp2k_traj.cell  \n")
        mdio_stream.write("&END CELL                      \n")
        mdio_stream.close()
        

        ################################
        # 2. Launch the actual job 
        ################################
    
        # Grab the necessary files
    
        helpers.run_bash_cmnd("cp " + ' '.join(glob.glob(args["basefile_dir"] + "/*")) + " .")
        
        ###
        ### Delete any not for this case (temperature)
        ###
        
        # Get a list of all cp2k.input files (differ by set temperature)
        
        cp2kins = sorted(glob.glob("*.cp2k.inp")) 
        
        # Determine the simulation tempertaure for this case

        tag = glob.glob("*#*xyz") # This block determines how many .xyz files there are for padding purposes
        tag = len(str(len(tag)))
        tag = "".zfill(tag+1)

        temp = str(int(float(helpers.head(glob.glob("*" + tag + "*xyz.xyz" )[0],2)[-1].split()[-2])))
        
        # Remove this case's temperature incar from the list of incars to delete
        
        cp2kins.remove(temp + ".cp2k.inp")
        helpers.run_bash_cmnd("rm -f " + ' '.join(cp2kins))
        
        ###
        ### Create the task string
        ###
                
        job_task = []
        job_task.append("module load " + args["modules"] + '\n')
    
    
        for k in range(len(atm_types)):
    
            job_task.append("ATOMS[" + repr(k) + "]=" + atm_types[k] + '\n')
    
        job_task.append("for j in $(ls *\#*xyz.xyz)         ")
        job_task.append("do                             ")
        job_task.append("    TAG=${j%*.xyz}             ")      
        job_task.append("    cp ${TAG}.xyz incfg.xyz    ")
        job_task.append("    cp ${TAG}.cell incfg.cell  ")
        job_task.append("    CHECK=${TAG}.cp2k_traj.forces      ")
        job_task.append("    if [ -e ${CHECK} ] ; then  ")  
        job_task.append("        continue               ")
        job_task.append("    fi                         ")
        job_task.append("    prev_tries=\"\"              ")
        job_task.append("    if [ -f ${TAG}.tries ] ; then     ")
        job_task.append("       prev_tries=`wc -l ${TAG}.tries | awk '{print $1}'`")
        job_task.append("       if [ $prev_tries -ge 2 ]; then ")
        job_task.append("            continue                   ")
        job_task.append("       fi                              ")
        job_task.append("    fi                                 ")
        job_task.append("    echo \"Attempt\" >> ${TAG}.tries")
        job_task.append("    TEMP=`awk '{if(NR==2){print $(NF-1);exit}}' incfg.xyz`")
        job_task.append("    TEMP=${TEMP%.*}")
        job_task.append("    cp ${TEMP}.cp2k.inp cp2k.inp       ")
        job_task.append("    rm -f cp2k.qm_basis-block.inp      ") 
        job_task.append("    for k in ${ATOMS[@]}               ")
        job_task.append("    do                                 ")
        job_task.append("        NA=`awk -v atm=\"$k\" \'{if((NR>2)&&($1==atm)){print 1;exit}}ENDFILE{print 0}\' incfg.xyz`")
        job_task.append("        if [ $NA -gt 0 ] ; then        ")
        job_task.append("            cat ${k}.cp2k.qm_basis-block.inp >> cp2k.qm_basis-block.inp ")
        job_task.append("        fi                             ")
        job_task.append("    done                               ")
        if args["job_system"] == "TACC":
            job_task.append("    ibrun " + "-n " + repr(int(args["job_nodes"])*int(args["job_ppn"])) + " " + args["job_executable"] + " -i cp2k.inp > ${TAG}.cp2k.out  ")
        else:
            job_task.append("    srun -N " + repr(args["job_nodes" ]) + " -n " + repr(int(args["job_nodes"])*int(args["job_ppn"])) + " " + args["job_executable"] + " -i cp2k.inp > ${TAG}.cp2k.out  ")
        
        job_task.append("    mv cp2k_traj.forces  ${TAG}.cp2k_traj.forces ")   
        job_task.append("done")
        
        this_jobid = helpers.create_and_launch_job(job_task,
            job_name       =          "cp2k_spcalcs"  ,
            job_email      =     args["job_email"   ] ,            
            job_nodes      = str(args["job_nodes"   ]),
            job_ppn        = str(args["job_ppn"     ]),
            job_walltime   = str(args["job_walltime"]),
            job_queue      =     args["job_queue"   ] ,
            job_account    =     args["job_account" ] ,
            job_system     =     args["job_system"  ] ,
            job_file       =     "run_cp2k.cmd",
            job_mem=args["job_mem"] if args["job_system"] == "UM-ARC" else None)
            
        run_cp2k_jobid.append(this_jobid.split()[0])    
    
        os.chdir(curr_dir)
    
    return run_cp2k_jobid        
