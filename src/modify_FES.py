import sys
import os
import helpers
import chimes_modify_FES
import dftbplus_modify_FES
import lmp_modify_FES

def clean_up(method):
    
    if method == "CHIMES":
         chimes_modify_FES.clean_up()
    elif method == "DFTB":
        dftbplus_modify_FES.clean_up()
    elif method == "LMP":
        lmp_modify_FES.clean_up()
    else:
        print("ERROR: Unknown method in modify_FES.py:",method)


def write_full_FES(traj_files):

    """
    
    Creates a b-labeled.txt file for a given set of trajectories
    
    """
    
    kcalpermolAng2HperB = 1/627.50960803/1.889725989 # Multiply a value in kcal/mol/Ang by this to get H/B

    traj_files = list(traj_files)
        
    # Process the trajectory file
    
    for i in range(len(traj_files)):
    
        if not os.path.isfile(traj_files[i]):
            print("\t***WARNING*** File",traj_files[i],"does not exist - assuming it is a dummy file!")
            continue
            
        print("\tOpening file:", "b-labeled_full.traj_file_idx-" + str(i)  + ".dat")
        helpers.run_bash_cmnd("rm -f b-labeled_full.traj_file_idx-" + str(i)  + ".dat")
        full = open("b-labeled_full.traj_file_idx-" + str(i)  + ".dat",'a')
            
        # Figure out what options the target .xyzf file has

        box_type, stress_type, energy_type = get_format(traj_files[i])
    
        # Process file frame by frame...
        
        natoms_per_frame = helpers.list_natoms(traj_files[i])
        nframes          = helpers.count_xyzframes_general(traj_files[i])
        
        ener = [None]*nframes
        sxx  = [None]*nframes; syy = [None]*nframes; szz = [None]*nframes; sxy = [None]*nframes; sxz = [None]*nframes; syz = [None]*nframes;

        start_line = 0

        for j in range(nframes):
    
            frame_fx = [0.0]*natoms_per_frame[j]
            frame_fy = [0.0]*natoms_per_frame[j]
            frame_fz = [0.0]*natoms_per_frame[j]

            # Parse and store info from the input.xyzf file
    
            nlines = 2+natoms_per_frame[j]

            contents = helpers.readlines(traj_files[i],start_line, start_line+nlines)
                        
            start_line += nlines
            
            boxline = contents[1].split()
            
            if energy_type == "yes":
                ener[j] = float(boxline.pop())
    
            if stress_type == "all":
                syz[j] = float(boxline.pop())
                sxz[j] = float(boxline.pop())
                sxy[j] = float(boxline.pop())
    
            if stress_type != "no":
                szz[j] = float(boxline.pop())
                syy[j] = float(boxline.pop())
                sxx[j] = float(boxline.pop())            
                

            for k in range(natoms_per_frame[j]):
            
                line = contents[k+2].split()

                full.write(line[0] + " " + str(float(line[4])/kcalpermolAng2HperB) + "\n")
                full.write(line[0] + " " + str(float(line[5])/kcalpermolAng2HperB) + "\n")
                full.write(line[0] + " " + str(float(line[6])/kcalpermolAng2HperB) + "\n")

            from_GPa = 6.9479
	    
            if stress_type == "all":	    
                full.write("s_xx " + str(sxx[j]/from_GPa) + "\n")
                full.write("s_xy " + str(sxy[j]/from_GPa) + "\n")
                full.write("s_xz " + str(sxz[j]/from_GPa) + "\n")
                full.write("s_yx " + str(sxy[j]/from_GPa) + "\n")
                full.write("s_yy " + str(syy[j]/from_GPa) + "\n")
                full.write("s_yz " + str(syz[j]/from_GPa) + "\n")
                full.write("s_zx " + str(sxz[j]/from_GPa) + "\n")
                full.write("s_zy " + str(syz[j]/from_GPa) + "\n")
                full.write("s_zz " + str(szz[j]/from_GPa) + "\n")

            elif stress_type != "no":	    
                full.write("s_xx " + str(sxx[j]/from_GPa) + "\n")
                full.write("s_yy " + str(syy[j]/from_GPa) + "\n")
                full.write("s_zz " + str(szz[j]/from_GPa) + "\n")


		
            if energy_type == "yes":	    
                full.write("+1 "  + str(ener[j]) + "\n")
                full.write("+1 "  + str(ener[j]) + "\n")
                full.write("+1 "  + str(ener[j]) + "\n")
            
        full.close()


def subtract_off(param_file, md_driver, method, traj_files, temper_files=None):

    """
    
    Subtracts force/energy/stress contributions predicted by a model specified in param_file, 
    from .xyzf files listed in *argv
    
    Expcts .xyzf file stresses in GPa, energies in kcal/mol, and forces in H/B
    
    Renames the original file "<original_name>.original
    Names the new file "<original_name>"
    
    Usage: subtract_off(param_file, md_driver, "CHIMES", ["traj-1.xyzf", "traj-2.xyzf",...], <kwargs>)
    
    Notes: See function definition in modify_FES.py for a full list of options. 
           Expects to be run from ???? folder           
    
    """
    
    kcalpermolAng2HperB = 1/627.50960803/1.889725989 # Multiply a value in kcal/mol/Ang by this to get H/B

    try:
        traj_files = list(traj_files)
    except:
        traj_files = None
        
    if temper_files is not None:
        temper_files = list(temper_files)
    
    # Read the parameter file and determine which atom types it describes
    
    atmtyps = None
    
    if method == "CHIMES":
        atmtyps = chimes_modify_FES.check_atomtypes(param_file)
    elif method == "DFTB":
        atmtyps = dftbplus_modify_FES.check_atomtypes(param_file)
    elif method == "LMP":
        atmtyps = lmp_modify_FES.check_atomtypes(param_file)
    else:
        print("ERROR: Unknown method in modify_FES.py:",method)


    print("Ignoring all atom types except:", atmtyps)
        
    # Process the trajectory file
    
    print("Will process traj files:\n\t",traj_files)
    
    
    for i in range(len(traj_files)):

        if not os.path.isfile(traj_files[i]):
            print("\t***WARNING*** File",traj_files[i],"does not exist - assuming it is a dummy file!")
            continue
    
        print("\t...Subtracting from file:",traj_files[i])
    
        helpers.run_bash_cmnd("rm -f subtracted.xyzf")
        ofstream = open("subtracted.xyzf",'a')
        
        print("\t\tReading temperatures from:",temper_files[i])
        
        temperature = 0.0
        if temper_files is not None:
            temperatures = helpers.readlines(temper_files[i])

        print("\t\tOpening file:","b-labeled_subtracted." + param_file.split("/")[-1] + ".traj_file_idx-" + str(i)  + ".dat")
        helpers.run_bash_cmnd("rm -f b-labeled_subtracted." + param_file.split("/")[-1] + ".traj_file_idx-" + str(i)  + ".dat")
        removed = open("b-labeled_subtracted." + param_file.split("/")[-1] + ".traj_file_idx-" + str(i)  + ".dat",'a')

        # Figure out what options the target .xyzf file has
    
        box_type, stress_type, energy_type = get_format(traj_files[i])
    
        # Process file frame by frame...
        
        natoms_per_frame = helpers.list_natoms(traj_files[i])
        nframes          = helpers.count_xyzframes_general(traj_files[i])
        
        ener = [None]*nframes
        sxx  = [None]*nframes; syy = [None]*nframes; szz = [None]*nframes; sxy = [None]*nframes; sxz = [None]*nframes; syz = [None]*nframes;
        fx   = []; fy  = []; fz  = [];
        
        start_line = 0

        for j in range(nframes):

            frame_fx = [0.0]*natoms_per_frame[j]
            frame_fy = [0.0]*natoms_per_frame[j]
            frame_fz = [0.0]*natoms_per_frame[j]

            # Parse and store info from the input.xyzf file
    
            nlines = 2+natoms_per_frame[j]

            contents = helpers.readlines(traj_files[i],start_line, start_line+nlines)
                        
            start_line += nlines
            
            # Remove atoms not described by parameter file
            
            popped = 0
            popped_data = []

            for k in range(natoms_per_frame[j]+1,1,-1):

                if contents[k].split()[0] not in atmtyps:
                    popped_data.insert(0,contents.pop(k))
                    frame_fx[k-2] = -1
                    frame_fy[k-2] = -1
                    frame_fz[k-2] = -1
                    popped += 1

            boxline = contents[1].split()
            
            if energy_type == "yes":
                ener[j] = float(boxline.pop())
                
            if stress_type == "all":
                syz[j] = float(boxline.pop())
                sxz[j] = float(boxline.pop())
                sxy[j] = float(boxline.pop())
                
            if stress_type != "no":
                szz[j] = float(boxline.pop())
                syy[j] = float(boxline.pop())
                sxx[j] = float(boxline.pop())            
                
            # Save the frame to a temporary .xyz file

            contents[0] = str(natoms_per_frame[j]-popped) +'\n'
            
            helpers.writelines("tmp.xyz",contents)
                
            # Obtain the corresponding F/E/S from the reference md code
            
            print("\t\t\t Running file:",traj_files[i],"frame",j, "with T = ",int(float(temperatures[j])))

            tmp_ener, tmp_stress, force_file = get_FES("tmp.xyz",param_file, md_driver, method, int(float(temperatures[j]))) 

            tmp_forces = helpers.readlines(force_file)
            
            # Update the forces, energies, and stresses
            
            if energy_type == "yes":
                ener[j] -= tmp_ener     ; ener[j] = str(ener[j])
            if stress_type != "no":
                sxx [j] -= tmp_stress[0]; sxx [j] = str(sxx [j])
                syy [j] -= tmp_stress[1]; syy [j] = str(syy [j])
                szz [j] -= tmp_stress[2]; szz [j] = str(szz [j])
                if stress_type == "all":
                    sxy [j] -= tmp_stress[3]; sxy [j] = str(sxy [j])
                    sxz [j] -= tmp_stress[4]; sxz [j] = str(sxz [j])
                    syz [j] -= tmp_stress[5]; syz [j] = str(syz [j])
            
            contents_idx = 0            
            popped_idx   = 0
                

            for k in range(len(frame_fx)):
            
                if frame_fx[k] == -1: # Then this atom didn't exist in the parameter file - no modification to forces
                
                    popped_line = popped_data[popped_idx].split()
                
                    removed.write(popped_line[0] + " 0.0\n")
                    removed.write(popped_line[0] + " 0.0\n")
                    removed.write(popped_line[0] + " 0.0\n")

                    popped_idx += 1
    
                    continue                    
                else:
                    line = contents[contents_idx+2].split()
                    
                    frame_fx[k] = str(float(line[4]) - float(tmp_forces[3*contents_idx  ])*kcalpermolAng2HperB)
                    frame_fy[k] = str(float(line[5]) - float(tmp_forces[3*contents_idx+1])*kcalpermolAng2HperB)
                    frame_fz[k] = str(float(line[6]) - float(tmp_forces[3*contents_idx+2])*kcalpermolAng2HperB)
                    
                    removed.write(line[0] + " " + tmp_forces[3*contents_idx  ])
                    removed.write(line[0] + " " + tmp_forces[3*contents_idx+1])
                    removed.write(line[0] + " " + tmp_forces[3*contents_idx+2])

                    contents_idx += 1    
                    
            from_GPa = 6.9479
                
            removed.write("s_xx " + str(tmp_stress[0]/from_GPa) + "\n")
            removed.write("s_xy " + str(tmp_stress[3]/from_GPa) + "\n")
            removed.write("s_xz " + str(tmp_stress[4]/from_GPa) + "\n")
            removed.write("s_yx " + str(tmp_stress[3]/from_GPa) + "\n")
            removed.write("s_yy " + str(tmp_stress[1]/from_GPa) + "\n")
            removed.write("s_yz " + str(tmp_stress[5]/from_GPa) + "\n")
            removed.write("s_zx " + str(tmp_stress[4]/from_GPa) + "\n")
            removed.write("s_zy " + str(tmp_stress[5]/from_GPa) + "\n")
            removed.write("s_zz " + str(tmp_stress[2]/from_GPa) + "\n")
            removed.write("+1 "  + str(tmp_ener)      + "\n")
            removed.write("+1 "  + str(tmp_ener)      + "\n")
            removed.write("+1 "  + str(tmp_ener)      + "\n")
            
            # Output the modified frame
            
            ofstream.write(str(natoms_per_frame[j]) + '\n')
            ofstream.write(' '.join(boxline) + ' ')
            
            if stress_type == "all":
                ofstream.write(sxx[j] + ' ' + syy[j] + ' ' + szz[j] + ' ' + sxy[j] + ' ' + sxz[j] + ' ' + syz[j] + ' ')
            elif stress_type == "diag":
                ofstream.write(sxx[j] + ' ' + syy[j] + ' ' + szz[j] + ' ')
            if energy_type == "yes":
                ofstream.write(ener[j])
            ofstream.write('\n')
            
            
            popped_idx   = 0
            contents_idx = 0
                
            for k in range(len(frame_fx)):
            
                if frame_fx[k] == -1: # Then this atom didn't exist in the parameter file - no modification to forces
                    ofstream.write(popped_data[popped_idx])
                    popped_idx += 1
                else:
                    line = contents[contents_idx+2].split()
                    idx  = k-2                
                    ofstream.write(' '.join(line[0:4]) + ' ' + frame_fx[k] + ' ' + frame_fy[k] + ' ' + frame_fz[k] + '\n')
                    contents_idx += 1
                
        ofstream.close()
        removed.close()
        helpers.run_bash_cmnd("cp " + traj_files[i] + " " + traj_files[i] + ".original")
        helpers.run_bash_cmnd("mv subtracted.xyzf " + traj_files[i])

            
def get_FES(xyz_file, param_file, md_driver, method, temperature=None):

    tmp_ener   = None
    tmp_stress = None
    force_file = None
    
    if method == "CHIMES":
        tmp_ener, tmp_stress, force_file = chimes_modify_FES.get_FES("tmp.xyz",param_file, md_driver) 
    elif method == "DFTB":
        tmp_ener, tmp_stress, force_file = dftbplus_modify_FES.get_FES("tmp.xyz",param_file, md_driver,temperature) 
    elif method == "LMP":
        tmp_ener, tmp_stress, force_file = lmp_modify_FES.get_FES("tmp.xyz",param_file, md_driver) 
    else:
        print("ERROR: Unrecognized method \"" + method + "\" for modify_FES.get_FES")
        print("Exiting.")
        exit()
        
    return tmp_ener, tmp_stress, force_file

    
def get_format(traj_file):

    """
    
    Reads a .xyzf file and determines its header format.
    
    Returns:
        1. A box type ("ortho" or non "ortho")
        2. A stress type ("all", "diag", or "no")
        3. An energy type ("yes" or "no")
    
    Usage: get_format(traj_file_name)
    
    
    Formats are based of presence of "NON_ORTHO" and number of fields, i.e.:
    
    
    17    NON_ORTHO ax ay az bx by bz cx cy cz sxx syy szz sxy sxz syz energy
    16    NON_ORTHO ax ay az bx by bz cx cy cz sxx syy szz sxy sxz syz
    14    NON_ORTHO ax ay az bx by bz cx cy cz sxx syy szz energy
    13    NON_ORTHO ax ay az bx by bz cx cy cz sxx syy szz
    11    NON_ORTHO ax ay az bx by bz cx cy cz energy
    10    NON_ORTHO ax ay az bx by bz cx cy cz
    
    10    x y z sxx syy szz sxy sxz syz energy
    9    x y z sxx syy szz sxy sxz syz
    7    x y z sxx syy szz energy
    6    x y z sxx syy szz
    4    x y z energy
    3    x y z
    
    
    """
    
    box_type    = None
    stress_type = None
    energy_type = None
    

    # Grab the header line
    
    ifstream = open(traj_file,'r')
    header   = ifstream.readline() # Ignore number of atoms
    header   = ifstream.readline()
    header   = header.split()
    hlen     = len(header)
    ifstream.close()
    
    # Parse
    
    if header[0] == "NON_ORTHO":
        box_type = "non_ortho"
    else:
        box_type = "ortho"
    
    # Determine stress/energy options            
    
    if   hlen == 17:
        stress_type = "all"
        energy_type = "yes"
    elif hlen == 16:
        stress_type = "all"
        energy_type = "no"        
    elif hlen == 14:
        stress_type = "diag"
        energy_type = "yes"
    elif hlen == 13:
        stress_type = "diag"
        energy_type = "no"        
    elif hlen == 11:
        stress_type = "no"
        energy_type = "yes"        
    elif hlen == 10:
        if box_type == "non_ortho":
            stress_type = "no"
            energy_type = "no"
        else:
            stress_type = "all"
            energy_type = "yes"            
    elif hlen == 9:
        stress_type = "all"
        energy_type = "no"        
    elif hlen == 7:
        stress_type = "diag"
        energy_type = "yes"
    elif hlen == 6:
        stress_type = "diag"
        energy_type = "no"        
    elif hlen == 4:
        stress_type = "no"
        energy_type = "yes"        
    elif hlen == 3:
        stress_type = "no"
        energy_type = "no"    
    
    return box_type, stress_type, energy_type    


def main():
    param_file = sys.argv[1]
    md_driver  = sys.argv[2]
    method     = sys.argv[3]
    traj_files = sys.argv[4:]
    
    print("Will subtract force, energy, and stress contributions arising from parameter file:", param_file)
    print("Will subtract from trajectory file(s):", traj_files)
    print("Will use the following MD driver:", md_driver)
    print("Expects driver is for method:", method)
    
    subtract_off(param_file, md_driver, method, traj_files)

if __name__ == "__main__":
    main()

        
