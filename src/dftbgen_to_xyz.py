import sys

def dftbgen_to_xyzf(genfile, resultstag, argv):

    """ 
    
    Run with: 
    
    #dftbgen_to_xyzf(["ENERGY","ALLSTR"], genfile="0000.gen", resultstag="results.tag")
    dftbgen_to_xyzf(<genfile>, <resultstag>, ["ENERGY","ALLSTR"])
    
    Only processes one file at a time
    Requires original genfile and results.tag
    Produces, e.g.,  0000.xyzf
    
    """
    
    ################################
    # 0. Set up an argument parser
    ################################
    
    ### ...argv
    
    args_targets = argv[0] # This is a pointer! ... specified whether/how to include stress & energy
    
    ################################
    # Read in the calculated energy, forces, and stress tensor
    ################################
    
    ifstream = open(resultstag,'r')
    results  = ifstream.readlines()
    ifstream.close()
    
    idx = [i for i, s in enumerate(results) if 'forces ' in s][-1]
    
    natoms = int(results[idx].split(',')[-1])
    energy = float(results[1])*627.50960803 # Convert from au (Hartree) to kcal/mol
    
    forces = results[idx+1:idx+1+natoms]
    
    idx = [i for i, s in enumerate(results) if 'stress ' in s][-1]
    
    stress = ""
    stress += results[idx+1]
    stress += results[idx+2]
    stress += results[idx+3]
    stress  = stress.split()
    
    stress = [ float(i)*29421.9091 for i in stress] # Convert from au H/b^3) to GPA        
    stress = [stress[0], stress[4], stress[8], stress[1], stress[2], stress[5]]
        
    ################################    
    # Read in the atom coordinates
    ################################
    
    ifstream = open(genfile,'r')
    results  = ifstream.readlines()
    ifstream.close()
    
    cell_a = results[-3].rstrip()
    cell_b = results[-2].rstrip()
    cell_c = results[-1].rstrip()

    symbols = results[2].split()
    
    coords  = results[3:]
    atomtyp = []
    
    for i in range(natoms): # Doesn't include atom type!
    
        atomtyp.append(coords[i].split()[1])
        
        coords[i] = ' '.join(coords[i].split()[2:])
        #units should already be correct
        #coords[i] = [float(i)*0.529177 for i in coords[i]]
        
    ################################
    # Generate the .xyzf file
    ################################
    
    outname = ''.join(genfile.split(".gen")) + ".xyzf"
        
    ofstream = open(outname,'w')

    ofstream.write(str(natoms) + '\n')
    
    boxline = "NON_ORTHO " + cell_a + " " + cell_b + " " + cell_c + " "
    
    if "ALLSTR" in argv:
        boxline = boxline + ' '.join(map(str,stress)) + " "
    elif "STRESS" in argv:
        boxline = boxline + ' '.join(map(str,stress[0:3])) + " "
    
    if "ENERGY" in argv:
        boxline  = boxline + str(energy)
        
        
    ofstream.write(boxline + '\n')
    
    for i in range(int(natoms)):
    
        ofstream.write(symbols[int(atomtyp[i])-1] + " ")
        
        ofstream.write(coords[i] + "  ")
        
        ofstream.write(forces[i])
        
    ofstream.close()
        

def dftbgen_to_xyz(*argv):

    # Warning: Currently assumes orthorhombic box!
    
    argv = list(argv)
    
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


if __name__ == "__main__":

    import sys
        
    dftbgen_to_xyz(*sys.argv[1:])
