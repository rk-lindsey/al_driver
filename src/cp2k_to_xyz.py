

def cp2k_to_xyzf(xyzfile, outfile, forcefile, argv):

    """
    jfdlskfjskldfjsl
    Run with:
    
    python cp2k2xyz.py <print stresses (true/false)> <print energies (true/false)>

    """
    
    # Extract the stress tensors

    tensors = []
    store  = -1 
    
    with open(outfile) as ifstream:
        for line in ifstream:
            if "STRESS| Analytical stress tensor [GPa]" in line:
                store += 1
            elif store == 0:
                store += 1
            elif store < 3:
                tensor.append(line.strip()[2:])
                store += 1
            if store > 3:
                store = -1
                tensors.append(tensor[0] + tensor[1] + tensor[3]) # Already in GPa
                tensor = []
    
    # Store the cell vectors
    
    cell = []
    
    cell += helpers.findinfile("CELL| Vector a [angstrom]",search_file).split([4:7]) 
    cell += helpers.findinfile("CELL| Vector b [angstrom]",search_file).split([4:7]) 
    cell += helpers.findinfile("CELL| Vector c [angstrom]",search_file).split([4:7]) 
    
                
    # Extract the energies 
    
    energies = helpers.findinfile("ENERGY| Total FORCE_EVAL ( QS ) energy [a.u.]: ",outfile)
    energies = [ float(i.split()[-1])*627.5096080305927 for i in energies ] # Convert from au to kcal/mol
    
    # Generate the .xyzf file
    
    crdstream = open(xyzfile,  'r')
    frcstream = open(forcefile,'r')
    xyzfstream = xyzfile.split(".xyz.xyz")
    xyzfstream = ''.join(xyzfstream) + ".xyz.xyzf"
    xyzfstream = open(xyzfstream,'w')

    natoms = int(helpers.head(xyzfile,1)[0])
    nlines = helpers.wc_l(xyzfile)
    frames = nlines/(natoms+2)
    
    for f in range(frames):
        
        xyzfstream.write(natoms+'\n')
        
        boxline = ' '.join(cell)
           
        if "ALLSTR" in argv:
            boxline = boxline + ' '.join(tensors[f]) + " "
        elif "STRESS" in argv:
            boxline = boxline + ' '.join(tensors[f][0:3]) + " "
        if "ENERGY" in argv:
            boxline  = boxline + str(energies[f])
        
        xyzfstream.write(boxline + '\n')
        
        crdstream.readline(); crdstream.readline()
        frcstream.readline(); frcstream.readline()
        
        for j in range(natoms):
        
            cline = crdstream.readline()
            fline = frcstream.readline()
            
            xyzfstream.write(cline + fline.split()[-3:] + '\n') # Already in H/B
            
    crdstream .close() 
    frcstream .close()
    xyzfstream.close()

if __name__ == "__main__":

    import sys
    
    # Called with cp2k_to_xyzf(xyzfile, outfile, forcefile, argv)
    # argv can contain ALLSTR, STRESS, and/or ENERGY
        
    cp2k_to_xyzf(*sys.argv[1:])