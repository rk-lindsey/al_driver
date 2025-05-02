# Global (python) modules

from subprocess import check_output 
from subprocess import CalledProcessError
import time
import glob
import sys
import math
import sys
import os

""" Small helper functions and utilities general to the ALC process. """

def findinfile(search_str,search_file):
    
    matches = []
    
    
    with open(search_file) as ifstream:
        for line in ifstream:
            
            if search_str in line:
                matches.append(line.strip())
    
    return matches
    
def getlineno(search_str,search_file):
    matches = []
    index   = 0
    with open(search_file) as ifstream:
        for line in ifstream:
            if search_str in line:
                matches.append(index)
            index += 1
                                                                    
    return matches  


def readlines(infile,start_line=0, nlines=-1):

    """ 
    
    A one-liner wrapper to open, readlines, and close a file
    
    Usage: readlines("my_file.txt") or readlines("my_file.txt",10)
           or readlines("my_file.txt",0,10)
    
    Notes: Outputs a list of lines corresponding to the contents of my_file.txt
           last two parameters specify which line to start read from (from zero),
           and how many lines to read
    
    WARNING: Entire file is read into memory - do not use with large files
    
    """
    
    ifstream = open(infile,'r')
    contents = ifstream.readlines()
    ifstream.close()
    
    if nlines<0:
        return contents
    else:
        return contents[start_line:nlines]

def appendlines(outfile,contents, nlines=-1):

    """ 
    
    A one-liner wrapper to open, append all contents of a list, and close a file
    
    Usage: writelines("my_file.txt") or writelines("my_file.txt",10)
    
    Notes: Make sure lines contain '\n'

    """    
    
    ofstream = open(outfile,'a')
    
    idx = 1
    
    for line in contents:
        ofstream.write(line)
        idx += 1
        
        if (nlines > 0) and (idx > nlines):
            break
        
    ofstream.close()
    
def writelines(outfile, contents, nlines=-1):

    """ 
    
    A one-liner wrapper to open, write all contents of a list, and close a file
    
    Usage: writelines("my_file.txt") or writelines("my_file.txt",10)
    
    Notes: Make sure lines contain '\n'

    """    
    
    ofstream = open(outfile,'w')
    
    idx = 1
    
    for line in contents:
        ofstream.write(line)
        idx += 1
        
        if (nlines > 0) and (idx > nlines):
            break
        
    ofstream.close()

def run_bash_cmnd(cmnd_str):

    """ 
    
    Runs a (bash) shell command - captures and returns any resulting output. 
    
    Usage: run_bash_cmnd("my command string")
    
    Notes: Linux wildcards will not work as expected. Use the glob if needed.
    
    """

    msg = ""

    try:
        msg = check_output(cmnd_str.split())
    except CalledProcessError as err_msg:
        msg = err_msg.output

    return msg.decode('utf-8')
    
def run_bash_cmnd_presplit(cmnd_str):

    """ 
    
    Runs a (bash) shell command - captures and returns any resulting output. 
    
    Usage: run_bash_cmnd(["my","pre-split", "string"])
    
    Notes: Linux wildcards will not work as expected. Use the glob if needed.
    
    """

    msg = ""
    
    try:
        msg = check_output(cmnd_str)
    except CalledProcessError as err_msg:
        msg = err_msg.output

    return msg.decode('utf-8')
    
def run_bash_cmnd_to_file(outfile, cmnd_str):

    """ 
    
    Runs a bash shell command - captures and saves any returned output to file. 
    
    Usage: run_bash_cmnd_to_file("my_outfile_name.dat", "my command string")
    
    Notes: Linux wildcards will not work as expected. Use the glob if needed.
    
    """
    
    ofstream = open(outfile,'w+')
    ofstream .write(run_bash_cmnd(cmnd_str))
    ofstream .close()
    
def cat_to_var(*argv):

    """ 
    
    Concatenates a list of files and returns result. 
    
    Usage: cat_to_var(file1.dat, file2.dat, file3.dat)    
    
    Notes: Linux wildcards will not work as expected. Use the glob if needed.
    
    """

    files_to_cat = argv # This is a pointer!
    
    contents = []
    
    for f in files_to_cat:
        
        ifstream = open(f,'r')
            
        contents += ifstream.readlines()    
            
        ifstream.close()
        
    return contents  
    
# def cat_specific(outfilename, *argv):

#     """ 
    
#     Concatenates a list of files and returns result. 
    
#     Usage: cat_specific("my_outfile.dat", "file1.dat", "file2.dat", "file3.dat")    
    
#     Notes: Linux wildcards will not work as expected. Use the glob if needed.
    
#     """
    
#     # Assumes first file is large, so avoids reading contents

#     files_to_cat = argv[0][0]

#     run_bash_cmnd("cp " + files_to_cat + " " + outfilename)
    
#     files_to_cat = argv[0][1:]

#     with open(outfilename, "a") as ofstream:
#         for f in files_to_cat:
        
#             with open(f, "r") as ifstream:
        
#                 if os.path.getsize(f)/1E9 > 15:

#                     for line in ifstream:
#                         ofstream.write(line)
#                 else:
#                     ofstream.write(ifstream.read()) # Memory issues with large files

def cat_specific(outfilename, *argv):
    """
    Concatenates a list of files using chunked reading and writing with 1GB chunks,
    interpreted as 1 billion bytes (10^9 bytes).
    This method is designed to prevent MemoryError while efficiently handling large files.
    
    Usage: 
        cat_specific("my_outfile.dat", ["file1.dat", "file2.dat", "file3.dat"])
    
    Notes:
        - The function operates in binary mode ('b'), ensuring that no data is lost or altered during the process.
        - It assumes that up to 1GB of memory in decimal notation (10^9 bytes) is acceptable per chunk.
    """
    
    # Set the chunk_size to 1GB, interpreted as 1 billion bytes (10^9).
    chunk_size = 10**9  # 1GB in bytes using decimal notation

    # Open the output file in binary write mode.
    with open(outfilename, "wb") as ofstream:
        # Iterate over each input filename provided in the argument list.
        for f in argv[0]:
            # Open each input file in binary read mode.
            with open(f, "rb") as ifstream:
                # Read the file in chunks until the end of file is reached.
                while True:
                    # Read a segment of the file into memory.
                    # The read operation is based on the number of bytes, and we're
                    # reading 1 billion bytes (or 1GB in decimal notation) at a time.
                    chunk = ifstream.read(chunk_size)
                    if not chunk:
                        # If the chunk is empty, we've reached the end of this file.
                        # Break out of the while loop and proceed to the next file.
                        break
                    # Write the chunk of data to the output file.
                    # The data is written as-is with no transformations or processing.
                    ofstream.write(chunk)

def cat_pattern(outfilename, pattern):

    """ 
    
    Concatenates files matching a linux pattern i.e. *, saves results to file. 
    
    Usage: cat_pattern("my_outfile.txt","*.dat")    
    
    Notes: Linux wildcards WILL work as expected. 
    
    """

    files_to_cat = sorted(glob.glob(pattern))
    
    with open(outfilename, "wb") as ofstream:

        for f in files_to_cat:

            with open(f, "rb") as ifstream:
                ofstream.write(ifstream.read())
                


def head(*argv):
    
    """ 
    
    Mimics functionality of Linux head command. 
    
    Usage: head("my_file.txt") or head("my_file.txt",2)
    
    Notes: Linux wildcards will not work as expected. Use the glob if needed.
    
    """    
    
    nlines = 10
    
    if len(argv) == 2:
        nlines = int(argv[1])
    elif len(argv) > 2:
        print("ERROR: Unrecognized head command: ", argv)
        exit()
        
    possible = wc_l(argv[0])
    
    if possible < nlines:
        nlines = possible
        
    ifstream = open(argv[0],'r')
    
    contents = []
    
    for i in range(nlines):
            contents.append(ifstream.readline())
    
    ifstream.close()
    
    return contents
    
def tail(*argv):
    
    """ 
    
    Mimics functionality of Linux tail command. 
    
    Usage: tail("my_file.txt") or tail("my_file.txt",2)
    
    Notes: Linux wildcards will not work as expected. Use the glob if needed.
    
    """    
    
    nlines = 10
    
    if len(argv) == 2:
        nlines = int(argv[1])
    elif len(argv) > 2:
        print("ERROR: Unrecognized head command: ", argv)
        exit()
    
    total_lines = wc_l(argv[0])
        
    ifstream = open(argv[0],'r')
    
    contents = []
    
    for i in range(total_lines):
    
        line = ifstream.readline()
        
        if i >= (total_lines - nlines):
            
            contents.append(line)
    
    ifstream.close()
    
    return contents    
    
def wc_l(infile):

    """ 
    
    Mimics functionality of Linux wc -l command. 
    
    Usage: wc_l("my_file.txt")
    
    Notes: Linux wildcards will not work as expected. Use the glob if needed.
    
    """    

    nlines = 0
    
    with open(infile, "r") as ifstream:
        for line in ifstream:
            nlines += 1
    return nlines        
    
def count_xyzframes_general(infile):

    """ 
    
    Counts the number of frames in a .xyz(f) file 
    
    Usage: count_xyzframes_general("my_file.xyz")
    
    Notes: Linux wildcards will not work as expected. Use the glob if needed.
    
    """    

    nframes = 0
    natoms  = []
    nlines  = 0
    
    with open(infile, "r") as ifstream:
        for line in ifstream:
            
            nlines +=1
        
            if len(line.split()) == 1:
                
                # Try/except for cases where print isn't finished
                
                try:
                    natoms.append(int(line.split()[0]))
                except:
                    break
                nframes += 1
                
    sanity = len(natoms)*2 + sum(natoms)
    
    # Check whether frame finished printing
    
    if sanity > nlines:
        nframes -= 1 
    
    
    return nframes    
    
def count_genframes_general(infile):

    """ 
    
    Counts the number of frames in a .gen file 
    
    Usage: count_xyzframes_general("my_file.gen")
    
    Notes: Linux wildcards will not work as expected. Use the glob if needed.
    
    """    

    nframes = 0
    natoms  = []
    nlines  = 0
    
    with open(infile, "r") as ifstream:
        for line in ifstream:
            
            nlines +=1
            
            splitline = line.split()
        
            if (len(splitline) == 2) and (splitline[-1] == "S"):
                nframes += 1
                natoms.append(int(line.split()[0]))
                
    sanity = len(natoms)*6 + sum(natoms)
    
    # Check whether frame finished printing
    
    if sanity > nlines:
        nframes -= 1 
    
    
    return nframes        
    
def list_natoms(infile):

    """ 
    
    Generates a list of the number of atoms in each frames of a .xyz(f) file 
    
    Usage: list_natoms("my_file.txt")
    
    Notes: Linux wildcards will not work as expected. Use the glob if needed.
    
    """    

    natoms = []
    
    with open(infile, "r") as ifstream:
        for line in ifstream:
            if len(line.split()) == 1:
                natoms.append(int(line.split()[0]))
    return natoms        
        
def email_user(base, address, status):

    """ 
    
    Sends a message (status) to the specified email address (address)
    
    Usage: email_user("me@my_domain.com","email message text")
    
    Notes: This uses (requires) linux mailx. Nothing will be sent if
           address is an empty string. Calls send_email.sh in utilities.

    """

    if address:

        cmnd = base + "/utilities/send_email.sh " + address + " " + status + " "

        return run_bash_cmnd(cmnd)
           
def create_and_launch_job(*argv, **kwargs):

    """ 
    
    Creates and submits a run file to the queuing system.
    
    Usage: create_and_launch_job(<arguments>)
    
    Notes: if "job_executable" is empty, uses the commands specified in *argv.
           See function definition in helpers.py for a full list of options.
           Currently, function only supports SLURM systems.
    
    """    

    ################################
    # 0. Set up an argument parser
    ################################
    
    default_keys   = [""]*12
    default_values = [""]*12

    # Overall job controls
    
    default_keys[0 ] = "job_name"          ; default_values[0 ] =     "ALC-x-lsq-1" # Name for ChIMES lsq job
    default_keys[1 ] = "job_nodes"         ; default_values[1 ] =     "2"            # Number of nodes for ChIMES lsq job
    default_keys[2 ] = "job_ppn"           ; default_values[2 ] =     "36"           # Number of processors per node for ChIMES lsq job
    default_keys[3 ] = "job_walltime"      ; default_values[3 ] =     "1"            # Walltime in hours for ChIMES lsq job
    default_keys[4 ] = "job_queue"         ; default_values[4 ] =     "pdebug"       # Queue for ChIMES lsq job
    default_keys[5 ] = "job_account"       ; default_values[5 ] =     "pbronze"      # Account for ChIMES lsq job
    default_keys[6 ] = "job_executable"    ; default_values[6 ] =     ""             # Full path to executable for ChIMES lsq job
    default_keys[7 ] = "job_system"        ; default_values[7 ] =     "slurm"        # slurm or torque    
    default_keys[8 ] = "job_file"          ; default_values[8 ] =     "run.cmd"      # Name of the resulting submit script    
    default_keys[9 ] = "job_email"         ; default_values[9 ] =     True           # Should emails be sent?
    default_keys[10] = "job_modules"       ; default_values[10] =     ""             # Name of the resulting submit script    
    default_keys[11] = "job_mem"           ; default_values[11] =     "128"             # GB
    

    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)
    
    ################################
    # 1. Create the job file
    ################################    
    
    
    run_bash_cmnd("rm -f " + args["job_file"])
    
    JOB = []
    JOB.append(" -J " + args["job_name"])
    JOB.append(" -N " + args["job_nodes"])
    JOB.append(" --ntasks-per-node " + args["job_ppn"])
    if args["job_mem"] and args["job_system"] == "UM-ARC":
        JOB.append("--mem-per-cpu="+str(int(int(args["job_mem"])/int(args["job_ppn"])))+"G")
    JOB.append(" -t " + args["job_walltime"])             
    JOB.append(" -p " + args["job_queue"])
    if args["job_email"]:
        JOB.append(" --mail-type=ALL")   
    JOB.append(" -A " + args["job_account"])  
    JOB.append(" -V " )
    JOB.append(" -o " + "stdoutmsg")
    
    ofstream = open(args["job_file"],'w')
    ofstream.write("#!/bin/bash\n")
    
    for i in range(len(JOB)):
    
        if args["job_system"] == "slurm" or "TACC" or "UM-ARC":
            JOB[i] = "#SBATCH" + JOB[i]
        elif args["job_system"] == "torque":
            JOB[i] = "#PBS"  + JOB[i]
        else:
            print("ERROR: Unknown job_system: ", args["job_system"])
            exit()
            
        ofstream.write(JOB[i] + '\n')
        
    if args["job_modules"]:
        ofstream.write("module load " + args["job_modules"] + '\n')
    
    if args["job_executable"]:
    
        ofstream.write(args["job_executable"] + '\n')
    else:
        job_list = argv[0]
        
        for i in range(len(job_list)):
            
            ofstream.write(job_list[i] + '\n')
    
    ofstream.close()
    
    ################################
    # 2. Launch the job file
    ################################

    jobid = None
    
    if args["job_system"] == "slurm" or args["job_system"] == "TACC" or args["job_system"] == "UM-ARC":
        jobid = run_bash_cmnd("sbatch " + args["job_file"]).split()[-1]
    else:    
        jobid = run_bash_cmnd("qsub " + args["job_file"])

    return jobid    
    
def wait_for_job(active_job, **kwargs):

    """ 
    
    Pauses the code until a single SLURM job completes.
    
    Usage: wait_for_job(2116091,<arguments>)
    
    Notes: Accepts a jobid and queries the queueing system to determine
           whether the job is active. Doesn't return until job completes.
           See function definition in helpers.py for a full list of options.
    
    """    

    ################################
    # 0. Set up an argument parser
    ################################

    default_keys   = [""]*3
    default_values = [""]*3
    
    default_keys  [0] = "job_system" ; default_values[0] = "slurm"
    default_keys  [1] = "verbose"    ; default_values[1] = False 
    default_keys  [2] = "job_name"   ; default_values[2] = "unspecified" 
    
    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)
    
    active_job = str(active_job).split()[0]
    
    
    ################################
    # 1. Determine job status, hold until complete
    ################################

    while True:
        
        check_job = ""
        
        if args["job_system"] == "slurm" or "TACC" or "UM-ARC":
            check_job = "squeue -j " + active_job
            
        elif args["job_system"] == "torque":
            print("ERROR: torque support not yet implemented in wait_for_job")
        else:
            print("ERROR: Unknown job_system: ", args["job_system"])
            exit()
            
        if active_job in  run_bash_cmnd(check_job):
        
            if args["verbose"]:
                print("Sleeping for 60 more seconds while waiting for job ", active_job, "...", args["job_name"])
        
            time.sleep(60) # sleep for 60 seconds
        else:        
            print("Breaking ... ")
            break                
            
    return
    
def wait_for_jobs(*argv, **kwargs):

    """ 
    
    Pauses the code until SLURM job completes.
    
    Usage: wait_for_jobs([2116091, 2116092], <arguments>)
    
    Notes: Accepts list of jobid and queries the queueing system to determine
           whether any jobs are active. Doesn't return until job completes.
           See function definition in helpers.py for a full list of options.
    
    """

    ################################
    # 0. Set up an argument parser
    ################################

    default_keys   = [""]*3
    default_values = [""]*3
    
    default_keys  [0] = "job_system" ; default_values[0] = "slurm"
    default_keys  [1] = "verbose"    ; default_values[1] = False 
    default_keys  [2] = "job_name"   ; default_values[2] = "unspecified" 
    
    args = dict(list(zip(default_keys, default_values)))
    args.update(kwargs)
    
    active_jobs = argv[0] # Pointer!
    

    ################################
    # 1. Determine job status, hold until complete
    ################################

    njobs  = len(active_jobs)

    active = [True]*njobs
    
    while True:
    
        for i in range(njobs):
            check_job = ""
            
            if type(active_jobs[i]) == type(1):
                active_jobs[i] = str(active_jobs[i])
        
            if args["job_system"] == "slurm" or "TACC":

                check_job = "squeue -j " + active_jobs[i]
            
            elif args["job_system"] == "torque":
                print("ERROR: torque support not yet implemented in wait_for_job")
            else:
                print("ERROR: Unknown job_system: ", args["job_system"])
                exit()
            
            if active_jobs[i] in  run_bash_cmnd(check_job):
                active[i] = True
            else:
                active[i] = False
            
        
        if True in active:
        
            if args["verbose"]:
                print("Sleeping for 60 more seconds while waiting for jobs ", active_jobs, "...", args["job_name"])
        
            time.sleep(60) # sleep for 60 seconds
        else:        
            print("Breaking ... ")
            break                    
    return  

def str2bool(v):

    """ 
    
    Converts "true" or "false" in any case to a corresponding boolean value.
    
    Usage: str2bool("FALSE")
    
    """

    return v.lower() in ("true")
    
def bool2str(v):

    """ 
    
    Converts a boolean type variable to the corresponding strings "true" or "false"
    
    Usage: bool2str(True)
    
    """
    
    if v:
        return "true"
    else:
        return "false"

def break_apart_xyz(*argv):

    """ 
    
    Breaks a .xyz(f) file into individual frames.
    
    Usage: break_apart_xyz(250, "my_file.xyz")
    
    Notes: Takes as input a number of frames and a .xyz or .xyzf file, and breaks it apart 
           into frames. 
           Optional: break into chunks of n frames (3rd arg).
           Optional: Save only the first frame of each chunk (True or False; 4th arg)
               
    """

    # Takes as input a number of frames and a .xyz or .xyzf file, and breaks it apart 
    # into frames. 

    # Optional: break into chunks of (3rd arg)


    print("Breaking apart file: ", argv[1])
    print("WARNING: Converting forces from Hartree/bohr to simulation units (kca/mol/Ang)")
    

    # How many frames are there? ... just do grep -F "Step" <file> | wc -l to find out
    FRAMES = int(argv[0])

    #########

    # What is the input .xyz file?
    XYZFILE = open(argv[1],"r")

    CHUNK_LEN = 1
    if len(argv) >= 3:
        CHUNK_LEN = int(argv[2])
        
    FIRST_ONLY = False
    if len(argv) >= 4:
        FIRST_ONLY = argv[3]

    #########

    ZEROES = len(str(FRAMES))+1

    for f in range(FRAMES):

        if f%CHUNK_LEN == 0:
        
            if f > 1:
                OFSTREAM.close()
                FRSTREAM.close()

            # Generate the output filename

            TAG = ""
            for i in range(ZEROES):
                if f == 0:
                    if f+1 < pow(10.0,i):
                        for j in range(ZEROES-i):
                            TAG += "0"
                        TAG += repr(f)
                        break
                    
                elif f < pow(10.0,i):
                    for j in range(ZEROES-i):
                        TAG += "0"
                    TAG += repr(f)
                    break

            OUTFILE  = argv[1]
            FORCES   = argv[1]
            TESTER   = OUTFILE [0:-4]
            TESTER   = TESTER  [-1]

            if TESTER == ".":
                FORCES   = OUTFILE[0:-5] + "_FORCES_#" + TAG + ".xyzf" 
                OUTFILE  = OUTFILE[0:-5] + "_#"        + TAG + ".xyzf" 
                
            else:
                FORCES   = OUTFILE[0:-4] + "_FORCES_#" + TAG + ".xyz" 
                OUTFILE  = OUTFILE[0:-4] + "_#"        + TAG + ".xyz" 
                

            OFSTREAM = open(OUTFILE,"w")
            FRSTREAM = open(FORCES,"w")
            
        if FIRST_ONLY and f%CHUNK_LEN > 0: # We still need to filter through ignored frames
        
            # Read the first line to get the number of atoms in the frame,
            # print back out to the xyzf file
        
            ATOMS = XYZFILE.readline()
        
            ATOMS = ATOMS.split()
        
            ATOMS = int(ATOMS[0])
        
            # Read/print the comment line

            XYZFILE.readline()

            # Now, read/print each atom line
        
            for j in range(ATOMS):
                XYZFILE.readline()
                
        else:
        
            # Read the first line to get the number of atoms in the frame,
            # print back out to the xyzf file
        
            ATOMS = XYZFILE.readline()
            
            OFSTREAM.write(ATOMS)
        
            ATOMS = ATOMS.split()
            
            ATOMS = int(ATOMS[0])
        
            # Read/print the comment line

            OFSTREAM.write( XYZFILE.readline())

            # Now, read/print each atom line
        
            for j in range(ATOMS):
        
                LINE = XYZFILE.readline()

                OFSTREAM.write(LINE)
            
                LINE = LINE.split()

                if len(LINE)>4:
                    FRSTREAM.write(repr(float(LINE[4])*(627.50960803*1.889725989)) + '\n')
                    FRSTREAM.write(repr(float(LINE[5])*(627.50960803*1.889725989)) + '\n')
                    FRSTREAM.write(repr(float(LINE[6])*(627.50960803*1.889725989)) + '\n')    
    return

def xyz_to_dftbgen(xyzfile):

    frames   = count_xyzframes_general(xyzfile)
    ifstream = open(xyzfile,'r')
    
    # Write the .gen file

    genfile  = '.'.join(xyzfile.split('.')[0:-1]) + ".gen"
    ofstream = open(genfile,'w')
    
    for f in range(frames):

        natoms  = int(ifstream.readline())
        boxline = ifstream.readline().split()
        
        a = [0.0]*3
        b = [0.0]*3
        c = [0.0]*3

        if boxline[0] == "NON_ORTHO":
            a[0] = float(boxline[1])
            b[1] = float(boxline[5])
            c[2] = float(boxline[9])
        
        else:
            a[0] = float(boxline[0])
            b[1] = float(boxline[1])
            c[2] = float(boxline[2])

        atom_types        = []
        unique_atom_types = []
        coords            = []        
        
        for i in range(natoms):
        
            line = ifstream.readline().split()
            atom_types.append(line[0])
            coords.append(' '.join(line[1:4]))
                
            unique_atom_types = list(set(atom_types))

        ofstream.write(str(natoms) + ' S\n')
        ofstream.write(' '.join(unique_atom_types) + '\n')

        for i in range(natoms):

            ofstream.write(str(i+1) + " " + str(unique_atom_types.index(atom_types[i])+1) + " " + coords[i] + "\n")
            
        ofstream.write("0.0 0.0 0.0\n")
        ofstream.write(' '.join(map(str, a)) + '\n')
        ofstream.write(' '.join(map(str, b)) + '\n')
        ofstream.write(' '.join(map(str, c)) + '\n')

    ifstream.close()
    ofstream.close()

    return genfile 
    
def get_xyz_boxdims(xyzfile, magnitudes=True):

    """ 
    
    Reads a .xyz file and returns two things:
    1. Is the box orthorhombic or triclinic
    2. boxdims, as strings
    
    The user specifies if they want magnitudes or latvectors (a 9-element list). 
    by default, returns magnitudes
    
    """

    boxdims = head(xyzfile,2)[-1].split()
    
    offdiag_elements = [1,2,3,5,6,7]

    
    is_ortho = True
    
    if boxdims[0] != "NON_ORTHO":
        if magnitudes: 
            return is_ortho, boxdims
        else:
           return is_ortho, [boxdims[0], "0.0", "0.0", "0.0", boxdims[1], "0.0", "0.0", "0.0", boxdims[2]]
    
    else:
       boxdims = boxdims[1:]
       
       for i in offdiag_elements:
           if abs(float(boxdims[i])) > 0.0001:
               is_ortho = False
       
       if not magnitudes:
           return is_ortho, boxdims
       elif magnitudes and not is_ortho:
           print("ERROR in helpers.get_xyz_boxdims: requested boxdims for an orthorhomic cell, but input cell is triclinic")
           print(xyzfile)
           print(boxdims)
           exit()
       else:
           return is_ortho, [boxdims[0], boxdims[4], boxdims[8]]

       
    
def dftbgen_to_xyz(*argv):

    """ 
    
    Converts a .gen file to .xyz and prints box lengths.
    
    Usage: dftbgen_to_xyz(250, "my_file.xyz")
    
    Notes: Assumes an orthorhombic box.
           Prints box lengths to a separate file (*.box).
               
    """

    #NOTE: Assumes an orthorhombic box

    # How many frames are there? ... just do grep -F "Step" <file> | wc -l to find out
    FRAMES = int(argv[0])

    # What is the input file?
    IFSTREAM = open(argv[1],"r")

    SKIP = 1
    if len(argv) == 3:
        SKIP = int(argv[2])

    # What is the outputfile
    OUTFILE  = argv[1]
    OUTFILE  = OUTFILE[0:-4] + ".xyz" # replace ".gen" with ".xyz"
    OFSTREAM = open(OUTFILE,"w")

    BOXFILE  = argv[1]
    BOXFILE  = BOXFILE[0:-4] + ".box" # replace ".gen" with ".xyz"
    BOXSTREAM = open(BOXFILE,"w")


    for i in range(FRAMES):
        
        # Read the first line to get the number of atoms in the frame
        
        ATOMS = IFSTREAM.readline()
        ATOMS = ATOMS.split()
        ATOMS = int(ATOMS[0])
        
        # Read the next line to get the atom types
        
        SYMBOLS = IFSTREAM.readline()
        SYMBOLS = SYMBOLS.split()
        
        # Print the header bits of the xyz file
        
        if (i+1)%SKIP == 0:
        
            OFSTREAM.write(repr(ATOMS) + '\n')
            OFSTREAM.write("Frame " + repr(i+1) + '\n')
        
        # Now read/print all the atom lines in the present frame
        
        for j in range(ATOMS):
        
            LINE = IFSTREAM.readline()
            LINE = LINE.split()
            
            # Replace the atom type index with a chemical symbol
        
            for k in range(len(SYMBOLS)):
                if k+1 == int(LINE[1]):
                    LINE[1] = SYMBOLS[k]
                    break
                    
            # Print out the line
            
            if (i+1)%SKIP == 0:
            
                OFSTREAM.write(' '.join(LINE[1:len(LINE)]) + '\n')
            
        # Finally, read the box lengths... assume cubic
        
        LINE = IFSTREAM.readline()    # Cell angles?
        
        LINE = IFSTREAM.readline().split()    
        X = LINE[0]
        
        LINE = IFSTREAM.readline().split()    
        Y = LINE[1]
        
        LINE = IFSTREAM.readline().split()    
        Z = LINE[2]    
        
        if (i+1)%SKIP == 0:
        
            BOXSTREAM.write(X + " " + Y + " " + Z + '\n')
            
    return

