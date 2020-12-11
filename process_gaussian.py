import os

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


	
	
def get_xyzf(logfile, comfile, natoms, boxls):

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
	
	for i in xrange(maxit-1,-1,-1):
	
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

	# Gaussian Atom Offset Energies (kcal/mol):
	E_GAUSS_C = -23716.035500449343
	E_GAUSS_N = -34217.444307885125
	E_GAUSS_O = -47066.163622356100

	# Vasp Atom Offset Energies (kcal/mol):
	E_VASP_C = -29.848029661940735
	E_VASP_N = -72.0692392257318
	E_VASP_O = -44.01350025037822
	
	n_C = 0
	n_N = 0
	n_O = 0
	
	
	for i in xrange(int(natoms)):
		if coords[i].split()[0] == "C":
			n_C += 1
		if coords[i].split()[0] == "N":
			n_N += 1
		if coords[i].split()[0] == "O":
			n_O += 1
			
	#print "Counted the following C N and O:", n_C, n_N, n_O
	#print "Gaussian energy was:", energy
			
	energy = energy - n_C*E_GAUSS_C - n_N*E_GAUSS_N - n_O*E_GAUSS_O
	
	#print "Gauss energy minus atom contributions is:",energy
	
	energy = energy + n_C*E_VASP_C  + n_C*E_VASP_N  + n_C*E_VASP_O	
	
	#print "VASP energy is:", energy
	
	ofstream = open(xyzfname,'w')
	ofstream.write(natoms + '\n')
	ofstream.write(boxls + " " + str(energy) + '\n')
	
	for i in xrange(int(natoms)):
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
		print check_job_success(sys.argv[1]) 
	
	if sys.argv[2] == "energy":
	
		if check_job_success(sys.argv[1]) == "success":
		
			print get_final_energy(sys.argv[1],"HF")
		else:
			print ""
			
	if sys.argv[2] == "xyzf":
		
		print get_xyzf(sys.argv[1],sys.argv[3], sys.argv[4], sys.argv[5:])
