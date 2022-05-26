import glob

import helpers

def clean_up():

    files   = ' '.join(glob.glob("*input.xyz"))
    files  += ' '.join(glob.glob("params* "))
    files  += ' '.join(glob.glob("*run_md.in"))
    files  += "run_chimesmd.cmd traj_bad_r.lt.rin.xyz traj_bad_r.lt.rin+dp.xyz restart.bak traj_bad_r.ge.rin+dp_dftbfrq.xyz traj.gen stdoutmsg run_md.out restart.xyzv md_statistics.out"

    helpers.run_bash_cmnd("rm -f " + files)

def check_atomtypes(param_file):

    
    param_file = helpers.readlines(param_file)
    
    natmtyps = int(param_file[[ i for i, s in enumerate(param_file) if 'ATOM TYPES:' in s ][-1]].split()[-1])
    atmtyps  = []
    
    for j in range(natmtyps):
        atmtyps.append(param_file[[ i for i, s in enumerate(param_file) if '# TYPEIDX #' in s ][-1]+j+1].split()[1])
    
    return atmtyps


def gen_input_file(param_file, xyz_file):
    
    """ 
    
    Creates a generic ChIMES_MD input file for a single point calculation,
    name run_md.in.
    
    Usage: gen_input_file(param_file, xyz_file)
    
    """
    
    ofstream = open ("run_md.in",'w')
    ofstream.write("\n# TEMPERA #\n\t0.0")
    ofstream.write("\n# CMPRFRC #\n\tfalse")
    ofstream.write("\n# TIMESTP #\n\t0.0")
    ofstream.write("\n# N_MDSTP #\n\t1")
    ofstream.write("\n# NLAYERS #\n\t1 REPLICATE 0")
    ofstream.write("\n# USENEIG #\n\ttrue")
    ofstream.write("\n# PRMFILE #\n\t" + param_file)
    ofstream.write("\n# CRDFILE #\n\t" + xyz_file)
    ofstream.write("\n# VELINIT #\n\tGEN")
    ofstream.write("\n# CONSRNT #\n\tNVT-MTK HOOVER 10")
    ofstream.write("\n# PRSCALC #\n\tANALYTICAL")
    ofstream.write("\n# FRQDFTB #\n\t1")
    ofstream.write("\n# ATMENER #\n\ttrue")
    ofstream.write("\n# FRQENER #\n\t1")    
    ofstream.write("\n# PRNTFRC #\n\ttrue 1")
    ofstream.write("\n# PRNTBAD #\n\tfalse")
    ofstream.write("\n# ENDFILE #")
    ofstream.write("\n#")
    ofstream.close()

def get_FES(xyz_file,param_file, md_driver):
    
    # Tasks:
    
    # Setup files for a ChIMES md run
    
    gen_input_file(param_file,xyz_file)
    
    # Run the single point calculation
    
    helpers.writelines("run_md.out",helpers.run_bash_cmnd(md_driver + " run_md.in"))
    
    # Parse/save the output
    
    natoms   = float(helpers.head(xyz_file,1)[0])    
    eperatm  = float(helpers.tail("md_statistics.out",1)[0].split()[3])
    tmp_ener = natoms*eperatm
    
    tmp_stress = helpers.tail("run_md.out",6)   
    
    for i in range(6):
        tmp_stress[i] = float(tmp_stress[i].split()[1])
    
    # Clean up
    
    #helpers.run_bash_cmnd("rm -f output.xyz.bak traj_bad_r.lt.rin.xyz traj_bad_r.lt.rin+dp.xyz traj_bad_r.ge.rin+dp_dftbfrq.xyz traj.gen run_md.out output.xyz md_statistics.out forceout.xyzf forceout-labeled.txt")
    
    # Return results
    
    return tmp_ener, tmp_stress, "forceout.txt"
