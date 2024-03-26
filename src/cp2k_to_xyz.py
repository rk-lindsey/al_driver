import helpers

def cp2k_to_xyzf(xyzfile, outfile, forcefile, argv):

    """
    jfdlskfjskldfjsl
    Run with:
    
    python cp2k2xyz.py <print stresses (true/false)> <print energies (true/false)>

    """
    
    # Extract the stress tensors

    tensor  = []
    tensors = []
    store   = -1 
    
    with open(outfile) as ifstream:
        for line in ifstream:
            if "STRESS| Analytical stress tensor [GPa]" in line:
                store += 1
            elif store == 0:
                store += 1
            elif (store >0) and (store < 4):
                tensor.append(line.split()[2:])
                store += 1
            if store > 3:
                store = -1
                # Output form should be xx,yy,zz,xy,xz,yz
                tensors.append([tensor[0][0]] + [tensor[1][1]] + [tensor[2][2]] + [tensor[0][1]] + [tensor[0][2]] + [tensor[1][2]]) # Already in GPa
                tensor = []
    
    # Store the cell vectors
    
    cell = []

    cell += helpers.findinfile("CELL| Vector a [angstrom]",outfile)[0].split()[4:7]
    cell += helpers.findinfile("CELL| Vector b [angstrom]",outfile)[0].split()[4:7]
    cell += helpers.findinfile("CELL| Vector c [angstrom]",outfile)[0].split()[4:7]
    
                
    # Extract the energies 
    
    energies = helpers.findinfile("ENERGY| Total FORCE_EVAL ( QS ) energy [a.u.]: ",outfile)
    energies = [ float(i.split()[-1])*627.5096080305927 for i in energies ] # Convert from au to kcal/mol
    
    # Generate the .xyzf file
    
    crdstream = open(xyzfile,  'r')
    frcstream = open(forcefile,'r')
    xyzfstream = xyzfile.split(".xyz")
    xyzfstream = ''.join(xyzfstream) + ".xyzf"
    xyzfstream = open(xyzfstream,'w')

    natoms = int(helpers.head(xyzfile,1)[0])
    nlines = helpers.wc_l(xyzfile)
    frames = int(nlines/(natoms+2))

    
    for f in range(frames):
        
        xyzfstream.write(str(natoms)+'\n')
        
        boxline = ' '.join(cell)
           
        if "ALLSTR" in argv:
            boxline = boxline + " " +  ' '.join(tensors[f])
        elif "STRESS" in argv:
            boxline = boxline + " " +' '.join(tensors[f][0:3])
        if "ENERGY" in argv:
            boxline  = boxline + " " + str(energies[f])
        
        xyzfstream.write("NON_ORTHO " + boxline + '\n')
        
        crdstream.readline(); crdstream.readline()
        frcstream.readline(); frcstream.readline()
        
        for j in range(natoms):
        
            cline = crdstream.readline()
            fline = frcstream.readline()
            
            xyzfstream.write(cline.rstrip() + " " + ' '.join(fline.split()[-3:]) + '\n') # Already in H/B
            
    crdstream .close() 
    frcstream .close()
    xyzfstream.close()

if __name__ == "__main__":

    import sys
    
    # Called with cp2k_to_xyzf(xyzfile, outfile, forcefile, argv)
    # argv can contain ALLSTR, STRESS, and/or ENERGY
        
    cp2k_to_xyzf(*sys.argv[1:])
