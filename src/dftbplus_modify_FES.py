import glob

import helpers

def clean_up():

    files  = ' '.join(glob.glob("*.sfk"))
    files += "tmp.gen detailed.out results.tag dftb.out tmp.xyz dftb_in.hsd stdoutmsg"


    helpers.run_bash_cmnd("rm -f " + files)

def check_atomtypes(parfile):

    atmtyps = []

    # Get a list of input files
    
    skf_files = sorted(glob.glob(parfile + "/*skf"))
    
    for i in range(len(skf_files)):
    
        tag = skf_files[i].split('/')[-1]
        tag = tag.split('-')    
        atmtyps.append(tag[0])
        tag = tag[1].split('.')
        atmtyps.append(tag[0])    
    
    atmtyps = list(set(atmtyps))
    atmtyps.sort()
    
    return atmtyps

def gen_input_file(xyz_file):
    
    """ 
    
    Converts user-provided xyz file to .gen
    
    Usage: gen_input_file(xyz_file)
    
    """

    return helpers.xyz_to_dftbgen(xyz_file) # Returns name of the xyz_file

def get_FES(xyz_file, param_file, md_driver, temperature):
    
    # Tasks:
    
    # Setup files for a dftbplus single point energy calculation
    # Assume user has specified the correct file format and provided 
    # all slater koster files
    # User should also set gen file to tmp.gen
    
    kcalpermolAng2HperB = 1/627.50960803/1.889725989 # Multiply a value in kcal/mol/Ang by this to get H/B
    
    #### NEED TO SET THE ELECTRON TEMPERATURE
    
    cmnd_1 = "cp " + param_file + "/" + str(temperature).strip() + ".dftb_in.hsd ./dftb_in.hsd"
    cmnd_2 = glob.glob(param_file + "/*skf")
    cmnd_2 = "cp " + ' '.join(cmnd_2) + " ."

    helpers.run_bash_cmnd(cmnd_1)
    helpers.run_bash_cmnd(cmnd_2)
    
    gen_file = gen_input_file(xyz_file)
    
    # Run the single point calculation
    
    helpers.writelines("dftb.out",helpers.run_bash_cmnd(md_driver))
    
    # Verify the job converged
    
    ifstream = open("dftb.out",'r')
    contents = ifstream.readlines()
    ifstream.close()
    
    for i in range(len(contents)):
        if "SCC is NOT converged, maximal SCC iterations exceeded" in contents[i]:
            print("        ERROR: DFTB+ job not converged within MaxSCCIterations.")    
            print("        ...try incresing SCCTolerance or Broyden MixingParameter, if using.")
            print("        Job:",xyz_file, "run in", helpers.run_bash_cmnd("pwd"))
            print("        Tailed output:")
            print(''.join(helpers.tail("dftb.out",25)))
            helpers.run_bash_cmnd("rm -f charges.bin tmp-broyden* dftb_pin.hsd dftbjob.gen geo_end.*")
            exit()
    
    # Parse/save the output
    
    # Energy and stress
    
    natoms = int(helpers.head(xyz_file,1)[0])

    ifstream = open("results.tag",'r')
    contents = ifstream.readlines()
    ifstream.close()
    
    energy     = None
    tmp_stress = []
    
    for i in range(len(contents)):
    
        if "total_energy" in contents[i]:
            tmp_ener = float(contents[i+1])*627.50960803
        if "stress" in contents[i]:
            sx = contents[i+1].split() # sxx, sxy, sxz
            sy = contents[i+2].split() # syx, syy, syz
            sz = contents[i+3].split() # szx, szy, szz
            
            # Convert stresses to GPa
            
            tmp_stress.append(float(sx[0])*29421.9091) # xx
            tmp_stress.append(float(sy[1])*29421.9091) # yy
            tmp_stress.append(float(sz[2])*29421.9091) # zz
            
            tmp_stress.append(float(sx[1])*29421.9091) # xy
            tmp_stress.append(float(sx[2])*29421.9091) # xz
            tmp_stress.append(float(sy[2])*29421.9091) # yz                    
    
    # Forces
    
    ifstream = open("detailed.out",'r')
    contents = ifstream.readlines()
    ifstream.close()


    kcalpermolAng2HperB = 1/627.50960803/1.889725989 # Multiply a value in kcal/mol/Ang by this to get H/B


    forces = []
    
    for i in range(len(contents)):
    
        if "Total Forces" in contents[i]:
        
            for j in range(natoms):
            
                temp = contents[i+j+1].split()

                forces.append(str(float(temp[0])/kcalpermolAng2HperB)+'\n')
                forces.append(str(float(temp[1])/kcalpermolAng2HperB)+'\n')
                forces.append(str(float(temp[2])/kcalpermolAng2HperB)+'\n')
                
    helpers.writelines("forceout.txt",forces)

    # Clean up
    
    helpers.run_bash_cmnd("rm -f charges.bin tmp-broyden* dftb_pin.hsd dftbjob.gen geo_end.*")
    
    # Return results
    
    return tmp_ener, tmp_stress, "forceout.txt"
