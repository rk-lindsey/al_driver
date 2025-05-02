import glob

import helpers

def clean_up():

    files   = ' '.join(glob.glob("*data.in"))
    files  += ' '.join(glob.glob("params* "))
    files  += ' '.join(glob.glob("*in.dallmps"))
    files  += "run_lmpmd.cmd *rank* traj_bad_r.lt.rin.xyz traj_bad_r.lt.rin+dp.xyz restart.bak traj_bad_r.ge.rin+dp_dftbfrq.xyz traj.lammpstrj stdoutmsg lmp.out out.lmp"

    helpers.run_bash_cmnd("rm -f " + files)

def check_atomtypes(param_file):

    
    param_file = helpers.readlines(param_file)
    
    natmtyps = int(param_file[[ i for i, s in enumerate(param_file) if 'ATOM TYPES:' in s ][-1]].split()[-1])
    atmtyps  = []
    
    for j in range(natmtyps):
        atmtyps.append(param_file[[ i for i, s in enumerate(param_file) if '# TYPEIDX #' in s ][-1]+j+1].split()[1])
    
    return atmtyps


def extract_masses(param_file,natomtyps):

    """

    Helper function for gen_input_file. Extracts atom type masses from the parameter file.

    """
    
    masses = []
    
    
    with open(param_file, 'r') as file:
        for line in file:  
    
            if "# TYPEIDX #" in line:
                for i in range(natomtyps):
                    line = file.readline()
                    masses.append(line.split()[-1])        
    return masses

def gen_input_file(param_file, xyz_file):
    
    """ 
    
    Creates a generic LAMMPS .in and .data file for a single point calculation,
    name lmp.in and data.in.
    
    Usage: gen_input_file(param_file, xyz_file)
    
    WARNING: This does not current support triclinic cells!
    
    """
    
    atmtyps = check_atomtypes(param_file)
    natoms  = str(helpers.head(xyz_file,1)[-1].strip())
    _, boxdims = helpers.get_xyz_boxdims(xyz_file) # ignores the first argument
    masses = extract_masses(param_file,len(atmtyps))
    
    
    ###### Generate the lmp.in file
    
    ofstream = open ("lmp.in",'w')
    ofstream.write("\nunits           real")
    ofstream.write("\nnewton          on")     
    ofstream.write("\natom_style      atomic")     
    ofstream.write("\natom_modify     sort 0 0.0") 
    ofstream.write("\nneighbor        0.01 bin")
    ofstream.write("\nread_data       data.in")
    ofstream.write("\npair_style      chimesFF") 
    ofstream.write("\npair_coeff      * * " + param_file)
    ofstream.write("\nfix             1 all nve")
    ofstream.write("\ncompute         ke_tensor all temp")
    ofstream.write("\nthermo_style    custom step time ke pe etotal temp press pxx pyy pzz pxy pxz pyz vol c_ke_tensor[1] c_ke_tensor[2] c_ke_tensor[3] c_ke_tensor[4] c_ke_tensor[5] c_ke_tensor[6]")
    ofstream.write("\nthermo_modify   line one format float %20.5f flush yes")
    ofstream.write("\nthermo          1")
    ofstream.write("\ndump            1 all custom 1 traj.lammpstrj id type element xu yu zu fx fy fz")
    ofstream.write("\ndump_modify     1 sort id element " + " ".join(atmtyps))
    ofstream.write("\ntimestep        0.1")
    ofstream.write("\nrun             0")
    ofstream.write("\n")
    ofstream.close()
    
    ###### Generate the data.in file
    
    ofstream = open ("data.in",'w')
    ofstream.write("Data file for " + xyz_file)
    ofstream.write("\n")
    ofstream.write("\n" + natoms + " atoms")
    ofstream.write("\n" + str(len(atmtyps)) + " atom types")
    ofstream.write("\n")
    ofstream.write("\n0.0 "+ boxdims[0] + " xlo xhi")
    ofstream.write("\n0.0 "+ boxdims[1] + " ylo yhi")
    ofstream.write("\n0.0 "+ boxdims[2] + " zlo zhi")
    ofstream.write("\n")
    ofstream.write("\nMasses")
    ofstream.write("\n")
    for i in range(len(atmtyps)):
        ofstream.write("\n" + str(i+1) + " " + masses[i])
    ofstream.write("\n")
    ofstream.write("\nAtoms")
    ofstream.write("\n")
    coords = helpers.tail(xyz_file,int(natoms))
    for i in range(len(coords)):
    
        line = coords[i].split()
	
        atmidx    = str(i+1)
        atmtypidx = str(atmtyps.index(line[0])+1)
        ofstream.write("\n" + atmidx + " " + atmtypidx + " " + " ".join(line[1:4]))
    ofstream.write("\n")
    ofstream.close()

def get_FES(xyz_file,param_file, md_driver):
    
    # Tasks:
    
    # Setup files for a LMP MD run
    
    gen_input_file(param_file,xyz_file)
    
    # Run the single point calculation
    
    helpers.writelines("lmp.out",helpers.run_bash_cmnd(md_driver + " -i lmp.in"))
    
    # Parse/save the output
    
    natoms   = int(helpers.head(xyz_file,1)[0])    
    
    tmp_ener    = float(helpers.head("log.lammps",helpers.getlineno("Step","log.lammps")[0]+2)[-1].split()[3])
    tmp_stress  = helpers.head("log.lammps",helpers.getlineno("Step","log.lammps")[0]+2)[-1].split()[7:13]
    
    # Convert LAMMPS pressure (atm, since real units) to GPa
    
    for i in range(len(tmp_stress)):
        tmp_stress[i] = float(tmp_stress[i])/9869.23

    coords = helpers.tail("traj.lammpstrj",natoms)

    ofstream = open("forceout.txt",'w')
    
    # modify_FES expects forces in kcal/mol
    #kcalpermolAng2HperB = 1/627.50960803/1.889725989 # Multiply a value in kcal/mol/Ang by this to get H/B
    
    
    for i in range(natoms):
        line = coords[i].split()[6:]
        ofstream.write(line[0] + "\n") # str(float(line[0])*kcalpermolAng2HperB) + "\n"
        ofstream.write(line[1] + "\n") # str(float(line[1])*kcalpermolAng2HperB) + "\n"
        ofstream.write(line[2] + "\n") # str(float(line[2])*kcalpermolAng2HperB) + "\n"
    ofstream.close()

    # Return results
    
    return tmp_ener, tmp_stress, "forceout.txt"
