import os

def parse_refdatafile(infile):

    """ 
    
    Parses a file containing Gaussian and planewave-code
    single atom energies. Format should be:
        
        # Comment lines start with \"#\"
        <chemical symbol> <Gaussian energy> <planewave code energy>
        
    Energies are expected in kcal/mol, and there should be an entry for each
    atom type of interest    
    
    """

    # Read file contents 

    ifstream = open(infile,'r')
    contents = ifstream.readlines()
    ifstream.close()
    
    # Remove comment lines
    
    tmp = []
    
    for i in range(len(contents)):
    
        if "#" in contents[i]:
            continue
            
        tmp.append(contents[i].rstrip())
        
    # Break up into atom type, Gaussian energy, and VASP energy
    
    atyps = []
    Gener = []
    Vener = []
    
    for i in range(len(tmp)):
    
        contents = tmp[i].split()
        
        if len(contents) < 1:
            continue
        
        atyps    .append(contents[0])
        Gener    .append(float(contents[1]))
        Vener    .append(float(contents[2]))
        
    # Output results
    
    return atyps, Gener, Vener 
         
    

def check_job_success(infile):

    """ 
    
    Checks termination status of a given Gaussian
    output file. Will return "success", "failure",
    or "incomplete"
        
    """ 

    succ_str = "Normal termination of Gaussian"
    fail_str = "Error termination via"

    with open(infile) as f:
    
        line = f.readline() # Info will never be in the first line, so don't process

        while line:
            
            line = f.readline()
            
            if   succ_str in line:
                return "success"
            elif fail_str in line:
                return "failure"
    return "incomplete"
            
def get_final_energy(infile,method):

    """
    
    <docstrings>
    
    """
    
    if not os.path.isfile(infile):
        return None
    
    
    contents = ""
    
    with open(infile) as f:
    
        line = f.readline() # Info will never be in the first line, so don't process
                
        while line:
            
            line = f.readline()    
            
            if "Unable to Open any file for archive entry." in line:
            
                contents += line.rstrip()
                
                while True:
                
                    line = f.readline()
                    
                    if "The archive entry for this job was punched." in line:
                        break
                    else:
                        contents += line.rstrip()    

    if contents == "":
        return None
    else:
    
        #print contents
        contents = contents.replace(" ", "") 
        contents = contents.split("\\")
        #contents = contents.replace(" ", "")     

        index    = [i for i, s in enumerate(contents) if 'HF' in s][0]
    
        return contents[index].split("=")[-1]


    
    
def get_xyzf(logfile, comfile, natoms, boxls, refdatafile):

    """
    
    docstrings...
    
    Note: Gaussian automatically deals with coords in ang and H/B for forces
    
    """

    coords = []
    forces = []
    #boxls = ' '.join(boxls)

    # Read the .com file, strip any empty lines
    
    comstream = open(comfile,'r')
    comdata   = comstream.readlines()
    comstream.close()
    
    maxit = len(comdata)
    
    for i in range(maxit-1,-1,-1):
    
        comdata[i] = comdata[i].rstrip()
        if len(comdata[i]) == 0:
            comdata.pop(i)
    
    coords = comdata[-1*int(natoms):]
    
    
    # Read the forces
    
    save_flag = 0
    
    with open(logfile) as f:
    
        line = f.readline() # Info will never be in the first line, so don't process
                
        while line:
            
            line = f.readline()
            
            if "Forces (Hartrees/Bohr)" in line:
                save_flag += 1
                
            elif save_flag > 0:
                save_flag += 1
                
            if (save_flag >= 4) and (save_flag < int(natoms)+5):
                
                forces.append(' '.join(line.split()[2:]))
    

    xyzfname = '.'.join(logfile.split('.')[:-1]) + ".xyzf"
    
    energy   = float(get_final_energy(logfile,"HF"))*627.509608030592 # This is the Gaussian energy in kcal/mol... need to correct for reference state


    atm_typs, E_GAUSS, E_VASP = parse_refdatafile(refdatafile)
    
    natm_typ = [1.0]*len(atm_typs)

    for i in range(int(natoms)):
    
        found = False
        
        for j in range(len(natm_typ)):
        
            tmp_typ = coords[i].split()[0]

            if tmp_typ == atm_typs[j]:
                natm_typ[j] += 1
                found = True
                
        if not found:
            print("ERROR: Could not find reference energies for atom type:", tmp_typ)
            print("       Check Gaussian energy to planewave input file")
            exit() 

    #print "Gaussian energy was:", energy
    
    for i in range(len(natm_typ)):

        energy -= natm_typ[i]*E_GAUSS[i]
        energy += natm_typ[i]*E_VASP[i]
                
    #print "Gauss energy minus atom contributions is:",energy
    
    #print "VASP energy is:", energy
    
    ofstream = open(xyzfname,'w')
    ofstream.write(natoms + '\n')
    ofstream.write(boxls + " " + str(energy) + '\n')
    
    for i in range(int(natoms)):
        ofstream.write(coords[i] + " " + forces[i] + '\n')
        
    ofstream.close()
    
    # return "file written: " + xyzfname
    return xyzfname

    


if __name__ == "__main__":

    """ 
    
    possible commands are: 
    
    python <this script> <logfile> check  # outputs success/failure/incomplete
    python <this script> <logfile> energy # outputs energy in kcal/mol
    python <this script> <logfile> xyzf   <comfile> <natoms> < boxlengths> # writes an xyf file
    
    WARNING: Assumes "HF" is the correct search term for energy
    WARNING: VASP and Gaussian atom energy offsets are hardcoded, and only for C,N,and O (PBEPBE/6-311+g(2d) EmpiricalDispersion=GD2)
    
    """
    
    if sys.argv[2] == "check":
        print(check_job_success(sys.argv[1])) 
    
    if sys.argv[2] == "energy":
    
        if check_job_success(sys.argv[1]) == "success":
        
            print(get_final_energy(sys.argv[1],"HF"))
        else:
            print("")
            
    if sys.argv[2] == "xyzf":
        
        print(get_xyzf(sys.argv[1],sys.argv[3], sys.argv[4], sys.argv[5:]))
