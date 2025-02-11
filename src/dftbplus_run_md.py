# Global (python) modules

import glob # Warning: glob is unserted... set my_list = sorted(glob.glob(<str>)) if sorting needed
import os

# Local modules

import helpers
import cluster

def post_proc(my_ALC, my_case, my_indep, *argv, **kwargs):

    """ 
    
    Post-processes a ChIMES MD run
    
    Usage: run_md(1, 0, 0, <arguments>)
    
    Notes: See function definition in run_md.py for a full list of options. 
           Requrires config.CHIMES_MOLANAL (should contain molanal.new and findmolecules.pl)
           Expects to be called from ALC-my_ALC's base folder.
           Assumes job is being launched from ALC-X.
           Supports ~parallel learning~ via file structure:
                  ALC-X/CASE-1_INDEP-1/<md simulation/stuff>
           Expects input files named like:
                  case-1.indep-1.input.xyz and case-1.indep-1.run_md.in
           will run molanal on finished simulation.
           Will post-process the molanal output.
           Will generate clusters.
           Will save clusters to CASE-X_INDEP-0/CFG_REPO.
               
    """
    
    ################################
    # 0. Set up an argument parser
    ################################
    
    ### ...argv
    
    args_species = argv[0] # This is a pointer!
    
    ### ...kwargs
    
    default_keys   = [""]*11
    default_values = [""]*11


    # MD specific controls
    
    default_keys[0 ] = "basefile_dir"  ; default_values[0 ] = "../CHIMES-MD_BASEFILES/"    # Directory containing run_md.base, etc.
    default_keys[1 ] = "driver_dir"    ; default_values[1 ] = ""                           # Post_proc_lsq*py file... should also include the python command
    default_keys[2 ] = "penalty_pref"  ; default_values[2 ] = 1.0E6                        # Penalty function pre-factor
    default_keys[3 ] = "penalty_dist"  ; default_values[3 ] = 0.02                         # Pentaly function kick-in distance
    default_keys[4 ] = "molanal_dir"   ; default_values[4 ] = ""                           # Path to the molanal directory
    default_keys[5 ] = "local_python"  ; default_values[5 ] = ""                           # Local computer's python executable

    # Cluster specific controls
        
    default_keys[6 ] = "do_cluster " ; default_values[6 ] = True                                              # Local computer's python executable
    default_keys[7 ] = "tight_crit"  ; default_values[7 ] = "../../../../tight_bond_crit.dat"                 # File with tight bonding criteria for clustering
    default_keys[8 ] = "loose_crit"  ; default_values[8 ] = "../../../../loose_bond_crit.dat"                 # File with loose bonding criteria for clustering
    default_keys[9 ] = "clu_code"     ; default_values[9 ] = "/p/lscratchrza/rlindsey/RC4B_RAG/11-12-18/new_ts_clu.cpp" # Clustering code
    default_keys[10] = "compilation" ; default_values[10] = "g++ -std=c++11 -O3"                              # Command to compile clustering code    

    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)

    ################################
    # 1. Move to the MD directory
    ################################
    
    my_md_path = "CASE-" + str(my_case) + "_INDEP_" + str(my_indep) + "/"

    os.chdir(my_md_path)
    
    ################################
    # 1. Run molanal
    ################################
    
    if os.path.isfile(args["basefile_dir"] + "case-" + str(my_case) + ".skip.dat"):
    
        helpers.run_bash_cmnd("cp " + args["basefile_dir"] + "case-" + str(my_case) + ".skip.dat skip.dat")
    
    
    # Copy/convert geo_end.xyz traj.gen
    
    box = []
    tmp = helpers.tail(args["basefile_dir"] + "case-" + str(my_case) + ".indep-" + str(my_indep) + ".gen",3)
    
    box.append(tmp[0].split()[0])
    box.append(tmp[1].split()[1])
    box.append(tmp[2].split()[2])
    box = ' '.join(box)
    
    frames = helpers.count_xyzframes_general("geo_end.xyz")

    ifstream = open("geo_end.xyz",'r')
    ofstream = open("traj.xyz",'w')

    for i in range(frames):
    
        # Natoms line
    
        line = ifstream.readline()
        ofstream.write(line)
        natoms = int(line)
        
        # boxlens line
        
        line = ifstream.readline()
        ofstream.write(box + '\n')
        
        # Coordinates
        
        for j in range(natoms):
            
            line = ifstream.readline()
            ofstream.write(line)
    
    helpers.xyz_to_dftbgen("traj.xyz")
        
    helpers.run_bash_cmnd_to_file("traj.gen-molanal.out",args["molanal_dir"] + "/molanal.new traj.gen")
    helpers.run_bash_cmnd_to_file("traj.gen-find_molecs.out", args["molanal_dir"] + "/findmolecules.pl traj.gen-molanal.out")
    helpers.run_bash_cmnd("rm -rf molecules " + ' '.join(glob.glob("molanal*")))

    print(helpers.run_bash_cmnd_presplit([args["local_python"], args["driver_dir"] + "/src/post_process_molanal.py"] + args_species))
    
    ################################
    # 2. Cluster
    ################################
    
    
    helpers.run_bash_cmnd("cp traj_bad_r.lt.rin+dp.cumul.xyz         traj_bad_r.lt.rin+dp.xyz")
    helpers.run_bash_cmnd("cp traj_bad_r.lt.rin.cumul.xyz            traj_bad_r.lt.rin.xyz")
    helpers.run_bash_cmnd("cp traj_bad_r.ge.rin+dp_dftbfrq.cumul.xyz traj_bad_r.ge.rin+dp_dftbfrq.xyz")

    cluster.get_pared_trajs(args["do_cluster"])
        
    if args["do_cluster"]:
        
        print("compilation: ", args["compilation"])
                
        cluster.generate_clusters(traj_file   = "traj_250F.xyz",
                      tight_crit  = args["tight_crit" ],
                      loose_crit  = args["loose_crit" ],
                      clu_code    = args["clu_code"   ],
                      compilation = args["compilation"])
        
    os.chdir("..")
    
    return     


def run_md(my_ALC, my_case, my_indep, *argv, **kwargs):

    """ 
    
    Launches a DFTB (+ChIMES) md simulation
    
    Usage: run_md(1, 0, 0, <arguments>)
    
    Notes: ???
               
    """
    
    ################################
    # 0. Set up an argument parser
    ################################
    
    
    ### ...argv
    
    #args_species = argv[0] # This is a pointer!
    
    ### ...kwargs
    
    default_keys   = [""]*16
    default_values = [""]*16

    # MD specific controls

    default_keys[0 ] = "basefile_dir"  ; default_values[0 ] = "../DFTB-MD_BASEFILES/"    # Directory containing run_md.base, etc.
    default_keys[1 ] = "driver_dir"    ; default_values[1 ] = ""                         # Post_proc_lsq*py file... should also include the python command
    default_keys[2 ] = "penalty_pref"  ; default_values[2 ] = 1.0E6                      # Penalty function pre-factor
    default_keys[3 ] = "penalty_dist"  ; default_values[3 ] = 0.02                       # Pentaly function kick-in distance
    default_keys[4 ] = "chimes_exe"    ; default_values[4 ] = None                       # Path to the ChIMES executable to be used - serial version preferred
    # Overall job controls

    default_keys[5 ] = "job_name"      ; default_values[5 ] = "ALC-"+ repr(my_ALC)+"-md"    # Name for ChIMES md job
    default_keys[6 ] = "job_nodes"     ; default_values[6 ] = "1"                            # Number of nodes for ChIMES md job
    default_keys[7 ] = "job_ppn"       ; default_values[7 ] = "1"                            # Number of processors per node for ChIMES md job
    default_keys[8 ] = "job_walltime"  ; default_values[8 ] = "1"                            # Walltime in hours for ChIMES md job
    default_keys[9 ] = "job_queue"     ; default_values[9 ] = "pdebug"                       # Queue for ChIMES md job
    default_keys[10] = "job_account"   ; default_values[10] = "pbronze"                      # Account for ChIMES md job
    default_keys[11] = "job_executable"; default_values[11] = ""                             # Full path to executable for ChIMES md job
    default_keys[12] = "job_system"    ; default_values[12] = "slurm"                        # slurm or torque    
    default_keys[13] = "job_file"      ; default_values[13] = "run.cmd"                     # Name of the resulting submit script
    default_keys[14] = "job_email"     ; default_values[14] = True                           # Send slurm emails?
    default_keys[15] = "job_modules"   ; default_values[15] = ""                             # Send slurm emails?

    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)    

    
    ################################
    # 1. Create the MD directory for this specific case and independent simulation, grab the base files
    ################################
    
    my_md_path = "CASE-" + str(my_case) + "_INDEP_" + str(my_indep) + "/"

    helpers.run_bash_cmnd("rm -rf " + my_md_path)
    helpers.run_bash_cmnd("mkdir -p " + my_md_path)

    # *dftb_in.hsd *K*gcc.gen
    helpers.run_bash_cmnd("cp "+ ' '.join(glob.glob(args["basefile_dir"] + "/case-" + str(my_case) + ".indep-" + str(my_indep) + ".dftb_in.hsd" )) + " " + my_md_path + "/dftb_in.hsd")
    helpers.run_bash_cmnd("cp "+ ' '.join(glob.glob(args["basefile_dir"] + "/case-" + str(my_case) + ".indep-" + str(my_indep) + ".gen" )) + " " + my_md_path)
    helpers.run_bash_cmnd("cp "+ ' '.join(glob.glob(args["basefile_dir"] + "/*skf")) + " " + my_md_path)
    helpers.run_bash_cmnd("cp "+ ' '.join(glob.glob(args["basefile_dir"] + "/bonds.dat"     )) + " " + my_md_path)
    helpers.run_bash_cmnd("cp "+ ' '.join(glob.glob(args["basefile_dir"] + "/run_molanal.sh")) + " " + my_md_path)
    helpers.run_bash_cmnd("cp "+ ' '.join(glob.glob(args["chimes_exe"])) + " " + my_md_path + "/chimes_md")
    helpers.run_bash_cmnd("cp "+ ' '.join(glob.glob(args["basefile_dir"] + "/run_md.in")) + " " + my_md_path)
    # Previous ALC ChIMES file
    helpers.run_bash_cmnd("cp GEN_FF/params.txt.reduced " + my_md_path)

    ################################
    # 2. Post-process the parameter file
    ################################
    
    os.chdir(my_md_path)
    
    ifstream   = open("params.txt.reduced",'r')
    paramsfile = ifstream.readlines()

    ofstream = open("tmp",'w')
    
    found = False
        
    for i in range(len(paramsfile)):
    
        if found:
            ofstream.write(paramsfile[i])
            ofstream.write("PAIR CHEBYSHEV PENALTY DIST:    " + str(args["penalty_dist"]) + '\n')
            ofstream.write("PAIR CHEBYSHEV PENALTY SCALING: " + str(args["penalty_pref"]) + '\n\n')

            found = False
        else:
    
            ofstream.write(paramsfile[i])
    
            if "FCUT TYPE" in paramsfile[i]:
                found  = True
    ofstream.close()
    helpers.run_bash_cmnd("mv tmp params.txt")
    
    
    ################################
    # 3. Post-process the run_md.in file
    ################################
    
    md_infile  = "dftb_in.hsd"
    md_xyzfile = "case-" + str(my_case) + ".indep-" + str(my_indep) + ".gen"  
    
    ifstream = open(md_infile,'r')
    runfile  = ifstream.readlines()
    
    ofstream = open("tmp",'w')    
    
    found1 = False
    found2 = False
    found3 = False
        
    for i in range(len(runfile)):
    
        if "RandomSeed" in runfile[i]:
            ofstream.write('  RandomSeed = ' + str(1+my_indep) + str(1+my_indep) + str(1+my_indep) + str(1+my_indep) + '\n')
        elif "<<<" in runfile[i]:
            ofstream.write("<<<\" " + md_xyzfile + "\"\n")
        else:
            ofstream.write(runfile[i])

                
    ofstream.close()
    helpers.run_bash_cmnd("mv tmp " + md_infile)

    
    ################################
    # 4. Launch the md simulation
    ################################
    
    
    # Create the task string
    
    job_task  = "-n 1 " + args["job_executable"] + " > dftb.out"    

    if (args["job_system"] == "slurm" or args["job_system"] == "UM-ARC"):
        job_task = "srun "   + job_task
    elif args["job_system"] == "TACC":
        job_task = "ibrun "  + job_task
    else:
        job_task = "mpirun " + job_task    
    
    md_jobid = helpers.create_and_launch_job(
        job_name       =     args["job_name"    ] ,
        job_email      =     args["job_email"   ] ,
        job_nodes      = "1",
        job_ppn        = "1",
        job_walltime   = str(args["job_walltime"]),
        job_queue      =     args["job_queue"   ] ,
        job_account    =     args["job_account" ] ,
        job_executable =     job_task,
        job_system     =     args["job_system"  ] ,
        job_modules    =     args["job_modules" ] ,
        job_file       =     "run_dftb.cmd")
        
    
    os.chdir("..")
    
    return md_jobid    
    
