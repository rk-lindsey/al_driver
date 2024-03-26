# Global (python) modules

import glob # Warning: glob is unsorted... set my_list = sorted(glob.glob(<str>)) if sorting needed
import os

# Localmodules

import helpers
import dftbgen_to_xyz

def cleanup_and_setup(*argv, **kwargs):

    """ 
    
    Removes DFTB-X folders, if they exist in the build_dir.
    
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

    # DFTB+ specific controls

    default_keys[0 ] = "build_dir"        ; default_values[0 ] = "."

    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)    

    for i in args_targets: # 20 all
    
        if args_this_case == -1:
    
            for i in args_targets: # 20 all

                dftb_dir = args["build_dir"] + "/DFTB-" + i
            
                if os.path.isdir(dftb_dir):
            
                    helpers.run_bash_cmnd("rm -rf " + dftb_dir)
                    helpers.run_bash_cmnd("mkdir  " + dftb_dir)
                                
                else:
                    helpers.run_bash_cmnd("mkdir  " + dftb_dir)
                
            return

    for i in args_targets: # 20 all
    
        if (i == "all") and (int(args_this_case) > 0):
            continue    

        dftb_dir = args["build_dir"] + "/DFTB-" + i
        
        if os.path.isdir(dftb_dir):
        
            helpers.run_bash_cmnd("rm -rf " + dftb_dir + "/*")

            dftb_dir = args["build_dir"] + "/DFTB-" + i + "/CASE-" + repr(args_this_case)

            if os.path.isdir(dftb_dir):
                helpers.run_bash_cmnd("rm -rf " + dftb_dir + "/*")
            else:
                helpers.run_bash_cmnd("mkdir  -p " + dftb_dir)
            
        else:
            helpers.run_bash_cmnd("mkdir -p  " + dftb_dir + "/CASE-" + repr(args_this_case))

def continue_job(*argv, **kwargs):

    """ 
    
    Checks whether all DFTB+ single point calculations ran, resubmits if needed.
    
    Usage: continue_job(<arguments>)
    
    Notes: See function definition in dftbplus_driver.py for a full list of options. 
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
    print("    Attempting to continue DFTB+ jobs for case: ", args_case)
    
    job_list = []
    
    for i in range(len(args_targets)): # 20 all
    
        if (args_targets[i] == "all") and (int(args_case) > 0):
            continue
    
        CASE_PATH = "CASE-" + repr(args_case)
    
        if os.path.isdir("DFTB-" + args_targets[i] + "/" + CASE_PATH):
        
            os.chdir("DFTB-" + args_targets[i] + "/" + CASE_PATH)

            # Count the number of possible jobs
            
            count_gen = len(glob.glob("case*.xyz.gen")) 
            
            # Check for convergence issues
            
            check_convergence(-1, args_case,args_targets, True) # First arg isn't used
            
            # Count the number of completed jobs
            
            count_tag = len(glob.glob("case*.tag"))

            print("")
            print("        Counted .gen:", count_gen)
            print("        Counted .tag:", count_tag)
            
            
            # If all jobs haven't completed, resubmit
            
            if count_gen > count_tag:
            
                print("            Resubmitting.")

                if args["job_system"] == "slurm":
                    job_list.append(helpers.run_bash_cmnd("sbatch run_dftb.cmd").split()[-1])
                else:    
                    job_list.append(helpers.run_bash_cmnd("qsub run_dftb.cmd").replace('\n', ''))

            else:
                print("            Not resubmitting.")
            
            print("")
            
            os.chdir("../..")
        else:
            print("Cant find directory DFTB-"+ args_targets[i] + "/" + CASE_PATH)
            print(helpers.run_bash_cmnd("pwd"))

    return job_list    

def check_convergence(my_ALC, *argv, **kwargs):

    """
    
    Checks whether DFTB+ jobs have completed within their requested SCF steps
    
    Usage: check_convergence(my_ALC, no. cases, dftb_job_types)
     
    # WARNING: This functionality is not used right now. If the DFTB job
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


    # DFTB+ specific controls
    
    # ...

    # Overall job controls    
    
    # ...
    
    #print helpers.run_bash_cmnd("pwd")
    
    #os.chdir("ALC-" + `my_ALC`)
    
    # FYI, if convergence not achieved within target SCC, dftb+ prints:
    # SCC is NOT converged, maximal SCC iterations exceeded
    
    
    ######
    # Generate a list of all DFTB+ jobs with n-SC > max SCC

    loc = helpers.run_bash_cmnd("pwd").strip()
    
    total_failed = 0
    
    prefix = ""
    
    for i in range(len(args_targets)): # 20 all
    
        if args_from: # Logic differs depending on whether called from continue_job (True) or check_convergence (False)
            prefix = "\t... (Convergence check): "    
            os.chdir("../..")

        if not os.path.isdir("DFTB-" + args_targets[i]):
    
            print("Skipping DFTB-" + args_targets[i])
        
            continue

                
        print(prefix + "Working on:","DFTB-" + args_targets[i])
    
        os.chdir("DFTB-" + args_targets[i])
        
        # Clear out the "tries" file so we try to achieve convergence one more time

        helpers.run_bash_cmnd("rm -f *.tries")
        
        # Build the list of failed jobs for the current DFTB job type (i.e. "all" or "20")
    
        base_list = []    

        iter_list = range(args_cases)
        
        if args_from:
            iter_list = range(args_cases,args_cases+1,1)
        
        for j in iter_list:
            
                tmp_list = sorted(glob.glob("CASE-" + repr(j) + "/*.dftb.out")) # list of all .dftb.out files for the current ALC's DFTB-20 or DFTB-all specific t/p case

                for k in range(len(tmp_list)):
                    with open(tmp_list[k]) as ifstream:
                        for line in ifstream:
                            if "SCC is NOT converged, maximal SCC iterations exceeded" in line:
                                base_list.append('.'.join(tmp_list[k].split(".")[0:4]))
                                break
        
        if len(base_list) > 0:
        
            print("Found",len(base_list),"job(s) with nSCC > MaxSCCIterations:")
            
            for j in range(len(base_list)):
                print("-",base_list[j])
            print("Declaring the problem impossible - renaming to *.ignored and skipping.")
        
        total_failed += len(base_list)
        
        # Renaiming corresponding .out and .tag files
        
        for j in range(len(base_list)):
            helpers.run_bash_cmnd("mv " + base_list[j] + ".dftb.out "    + base_list[j] + ".ignored")
            #helpers.run_bash_cmnd("mv " + base_list[j] + ".results.tag " + base_list[j] + ".ignored") # File not generated if nSCC > max
            helpers.run_bash_cmnd("mv " + base_list[j] + " "             + base_list[j] + ".ignored")
            helpers.run_bash_cmnd("mv " + base_list[j] + ".gen  "        + base_list[j] + ".ignored")            


    total_failed = 0
    
    os.chdir(loc)
    
    
    return  total_failed

def generate_gen(inxyz, *argv):

    """ 
    
    Converts a .xyz file to a DFTB+ .gen file.
    
    Usage: (my_file./usr/workspace/wsb/rlindsey/AL_Driver_SVN/rlindsey_branch/xyz, ["C","O"], 6500) # , [1,2])
    
    Notes: The second argument is list of atom types
           The final argument is the smearing temperature, in Kelvin
              
    """

    atm_types = argv[0] # pointer!
    smearing  = float(argv[1])
    ifstream  = open(inxyz,'r')
    ofstream  = open(inxyz + ".gen", 'w')
    
    # Set up the header portion
        
    box = ifstream.readline()        # No. atoms
    box = ifstream.readline().split()    # Box lengths
        
    a = [0.0]*3
    b = [0.0]*3
    c = [0.0]*3
    
    if box[0] == "NON_ORTHO":
        
        for i in range(3):
            
            a[i] = box[1+i]
            b[i] = box[1+i+3]
            c[i] = box[1+i+6]
    else:
    
        print(box)
        a[0] = box[0]
        b[1] = box[1]
        c[2] = box[2]
        
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
    
    ofstream.write(str(sum(natm_types)) + " S\n")
    ofstream.write("# " + str(smearing) + " K\n")
    ofstream.write(' '.join(atm_types) + '\n')
    
    for i in range(len(contents)):
        
        line = contents[i].split()                
        line = str(i+1) + " " + str(atm_types.index(line[0])+1) + " " +  ' '.join(line[1:]) + '\n'
        ofstream.write(line)
    
    ofstream.write("0.0 0.0 0.0\n")    
    
    ofstream.write(' '.join(map(str,a)) + '\n')
    ofstream.write(' '.join(map(str,b)) + '\n')
    ofstream.write(' '.join(map(str,c)) + '\n')
            
    ofstream.close()

def post_process(*argv, **kwargs):

    """ 
    
    Converts a converts a DFTB+ .gen file to .xyzf file
    
    Usage: post_process(<arguments>)
    
    Notes: See function definition in dftbplus_driver.py for a full list of options. 
               
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


    # DFTB specific controls
    
    default_keys[0 ] = "dftb_postproc"  ; default_values[0 ] = ""        # Parses a results.tag for E and stress tensor and detailed.out for forces     

    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)    
    
    ################################

    for i in range(len(args_targets)): # 20 all

        if not os.path.isdir("DFTB-" + args_targets[i]):
        
            print("Skipping DFTB-" + args_targets[i])
            
            continue

            
        print("Working on:","DFTB-" + args_targets[i])
    
        os.chdir("DFTB-" + args_targets[i])
    
        helpers.run_bash_cmnd("rm -f OUTCAR.xyzf")
        
        dftb_out_list = []
        gencoord_list = []
        resulttg_list = []
        
        for j in range(args_cases):
        
            gencoord_list += sorted(glob.glob("CASE-" + repr(j) + "/*xyz.gen"))
            resulttg_list += sorted(glob.glob("CASE-" + repr(j) + "/*.results.tag"))
            dftb_out_list += sorted(glob.glob("CASE-" + repr(j) + "/*.dftb.out"))
            
            if len(gencoord_list) != len(resulttg_list):
                print("ERROR: In dftbplus_driver.post_process on case",j)
                print("       Number of .gen files and .results.tag files do not match")
                print("       Something went wrong with DFTB calculations...")
                exit()
                
        for j in range(len(resulttg_list)):

            dftbgen_to_xyz.dftbgen_to_xyzf(gencoord_list[j], resulttg_list[j], args_properties)
            
            outfile = gencoord_list[j].split(".xyz.gen")
            outfile = ''.join(outfile) + ".xyz.xyzf"
            
            # Figure out the temperature
            
            tmpfile = open(dftb_out_list[j],'r')
            tmpdata = tmpfile.readlines()
            tmpfile.close()
            
            tmp_temp = None

            for line in tmpdata:
                
                if "Electronic temperature:" in line:
                
                    tmp_temp = str(int(float(line.split()[-1])*315777.09))
                    break

            tmpfile = gencoord_list[j].split(".xyz.gen")
            tmpfile = ''.join(outfile) + ".xyz.temps"
            tmpstream = open(tmpfile,'w')
            tmpstream.write(tmp_temp + '\n')
            tmpstream.close()
            
            ###
            
            if "ENERGY" in args_properties: # Make sure the configuration energy is less than or equal to zero
            
                tmp_ener = helpers.head(outfile,2)
                tmp_ener = float(tmp_ener[1].split()[-1])
                
                if tmp_ener >= 0.0:
                    
                    print("Warning: DFTB energy is positive energy for job name", resulttg_list[j], ":", tmp_ener, "...skipping.")
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
         
def setup_dftb(my_ALC, *argv, **kwargs):

    """ 
    
    Sets up and launches DFTB+ single point calculations
    
    Usage: setup_dftb(1, <arguments>)
    
    Notes: See function definition in dftbplus_driver.py for a full list of options. 
           Expects to be run from the ALC-X folder.
           Expects the "all" file in the ALC-X folder.
           Expects the "20" file in the ALC-X/INDEP_X folder.
           Requries a list of atom types.
           
               Expects a dftb_in.hsd file for each state point temperature considered, 
           named like: <smearing t in K>.dftb_in.hsd, stored in config.DFTB_FILES.
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


    # DFTB specific controls
    
    default_keys[0 ] = "basefile_dir"  ; default_values[0 ] = "../QM_BASEFILES/"  # dftb_in.hsd files, optionall .sfk files
    default_keys[1 ] = "traj_list"     ; default_values[1 ] = "traj_list.dat"     # Traj_list used in fm_setup.in... last column is target temperatura
    default_keys[2 ] = "modules"       ; default_values[2 ] = "mkl"               # Post_proc_lsq*py file... should also include the python command
    default_keys[3 ] = "build_dir"     ; default_values[3 ] = "."                 # Post_proc_lsq*py file... should also include the python command
    default_keys[4 ] = "first_run"     ; default_values[4 ] = False               # Optional... is this the first run? if so, dont search for "CASE" in the name


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
    
    
    run_dftb_jobid = []
    
    ################################
    # 1. Set up and launch the dftb+ single point calculations
    ################################
        
    for i in range(len(args_targets)): # 20 all
    
        if (args_targets[i] == "all") and (int(my_case) > 0):
            continue    
    
        curr_dir = helpers.run_bash_cmnd("pwd").rstrip() # This should be either CASE-X... (ALC>=1) or ...? (ALC==0)
    
        dftb_dir = "DFTB-" + args_targets[i] + "/CASE-" + my_case
        
        helpers.run_bash_cmnd("mkdir -p " + dftb_dir)        
            
        # Set up an launch the job
        
        os.chdir(dftb_dir)
        
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
            
            # Check whether there's even anything in the file. If not, skip
            
            try:
                atoms  = helpers.head(my_file,1)[0].rstrip()
            except:
                print("Warning: No configurations found for case " + str(my_case))
                print("\tSearched file:",my_file, ", which is based on \"all\" and \"20\" trajectories")
                continue
                
            frames = helpers.wc_l(my_file  )
            frames = frames / (2+int(atoms))

            helpers.break_apart_xyz(frames, my_file)
            
            helpers.run_bash_cmnd("rm -f " + ' '.join(glob.glob("*FORCES*")))
            
            temp = my_smear

            # Generate the .gen files

            target_files = ' '.join(sorted(glob.glob("case_" + str(my_case) + ".indep_0.traj_" + args_targets[i] + "F_#*"))).split()

            for j in target_files:
            
                if my_smear == "TRAJ_LIST":

                    temp = int(temps[int(my_case)][2])
                    
                print("\tOn case",my_case,"configuration",j,"generating .gen with smearing temperature:",temp)

                generate_gen(j, atm_types, temp)    
                
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
                            
                print("\tOn case",my_case,"configuration",sel_file,"generating .gen with smearing temperature:",temp)

                generate_gen(curr_dir + "/" + sel_file, atm_types, temp)

                helpers.run_bash_cmnd("mv " + curr_dir + "/" + sel_file + ".gen tmp.gen")
                
    
                sel_gen = sel_file + ".gen"
                sel_gen = sel_gen.replace('/','.')
                
                helpers.run_bash_cmnd("mv  tmp.gen " + sel_gen)


        ################################
        # 2. Launch the actual job 
        ################################
    
        # Grab the necessary files
    
        helpers.run_bash_cmnd("cp " + ' '.join(glob.glob(args["basefile_dir"] + "/*")) + " .")
    
        # Create the task string
                
        job_task = []
        job_task.append("module load " + args["modules"] + '\n')

        job_task.append("for j in $(ls *xyz.gen)              ")    
        job_task.append("do    ")
        job_task.append("    rm -f charges.bin tmp-broyden* dftb_pin.hsd dftbjob.gen geo_end.*")
        job_task.append("    if [[ $j == \"dftbjob.gen\" ]] ; then continue; fi")
        job_task.append("    TAG=${j%*.gen}              ")    
        job_task.append("    cp ${TAG}.gen dftbjob.gen ")
        job_task.append("    CHECK=${TAG}.results.tag  ")
        job_task.append("    if [ -e ${CHECK} ] ; then ")    
        job_task.append("        l=`wc -l ${TAG}.dftb.out | awk '{print $1}'` ")    
        job_task.append("        if [ $l -gt 0 ] ; then  ")            
        job_task.append("            continue    ")    
        job_task.append("        fi         ")    
        job_task.append("    fi            ")
        job_task.append("    TEMP=`awk '{if(NR==2){print int($(NF-1)); exit}}' dftbjob.gen`")
        job_task.append("    cp " + args["basefile_dir" ] + "/${TEMP}.dftb_in.hsd dftb_in.hsd        ")    
        job_task.append("    srun -N " + str(args["job_nodes" ]) + " -n " + str(int(args["job_nodes"])*int(args["job_ppn"])) + " " + args["job_executable"] + " > ${TAG}.dftb.out  ")        
        job_task.append("    mv results.tag ${TAG}.results.tag")
        job_task.append("    mv md.out      ${TAG}.md.out     ")
        job_task.append("done    ")
        job_task.append("rm -f charges.bin tmp-broyden* dftb_pin.hsd dftbjob.gen geo_end.*")    

        
        this_jobid = helpers.create_and_launch_job(job_task,
            job_name       =          "dftb_spcalcs"  ,
            job_email      =     args["job_email"   ] ,            
            job_nodes      = str(args["job_nodes"    ]),
            job_ppn        = str(args["job_ppn"    ]),
            job_walltime   = str(args["job_walltime"]),
            job_queue      =     args["job_queue"    ] ,
            job_account    =     args["job_account" ] ,
            job_system     =     args["job_system"  ] ,
            job_mem        =     args["job_mem"     ],
            job_file       =     "run_dftb.cmd")
            
        run_dftb_jobid.append(this_jobid.split()[0])    
    
        os.chdir(curr_dir)
    
    return run_dftb_jobid    
