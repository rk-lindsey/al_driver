import os
import glob
import helpers

def check_convergence(my_ALC, *argv, **kwargs):

	"""
	
	Checks whether vasp jobs have completed within their requested NELM
	
	Usage: check_convergence(my_ALC, no. cases, VASP_job_types)
	
	Notes: VASP_job_types can be ["all"], ["all","20"] or ["20"]
	       
	WARNING: Deletes OUTCARs, modifies *.INCARS
	
	"""
	
	# Developer notes: vasp_driver.continue_job counts *.POSCARS and *.OUTCARS.
	# If !=, then simply resubs the .cmd file and lets the .cmd file take care 
	# of the rest of the logic. The .cmd file also looks to see if *.OUTCAR 
	# existis. If it does, it skips the job. otherwise, copies 
	# <temperature>.incar to incar and builds the corresponding POTCAR
	#
	# So what this function does is  delete the corresponding .OUTCARS, and then 
	# edits all .INCAR's to have IALGO = 38
	#
	# Once run, should just be able to call vasp_driver.continue_job as normally
	# done in main.py		

	
	################################
	# 0. Set up an argument parser
	################################
	
	### ...argv

	args_cases   = argv[0]	
	args_targets = argv[1] # ... all ... 20


	# VASP specific controls
	
	# ...

	# Overall job controls	
	
	# ...
	
	os.chdir("ALC-" + `my_ALC`)
	
	total_failed = 0
	
	
	################################
	# Generate a list of all VASP jobs with n-SC >= NELM
	################################

	for i in xrange(len(args_targets)): # 20 all

		if not os.path.isdir("VASP-" + args_targets[i]):
	
			print "Skipping VASP-" + args_targets[i]
		
			continue

		
		print "Working on:","VASP-" + args_targets[i]
	
		os.chdir("VASP-" + args_targets[i])
		
		# Build the list of failed jobs for the current VASP job type (i.e. "all" or "20")
	
		base_list = []
		
		for j in xrange(args_cases):
		
		        tmp_list = sorted(glob.glob("CASE-" + `j` + "/*.OUTCAR")) # list of all .outcar files for the current ALC's VASP-20 or VASP-all specific t/p case
		        
		        for k in xrange(len(tmp_list)):
		        
		        	# Get max NELM
		        
		        	NELM = None
				
		        	with open(tmp_list[k]) as ifstream:
		        	
		        		for line in ifstream:
		        			
		        			if "   NELM   =    " in line:
		        			
		        				NELM = int(line.split()[2].strip(';'))
		        				break
		        				
		        	# Determine if job failed because NELM reached
		        	
		        	oszicar  = tmp_list[k].split(".OUTCAR")[0] + ".OSZICAR"
		        	last_rmm = int(helpers.tail(oszicar,2)[0].split()[1])
				
				#print last_rmm, NELM
		        	
		        	if last_rmm >= NELM:
		        		base_list.append(tmp_list[k].split(".OUTCAR")[0]) # Won't include the final extension (e.g. POSCAR, OSZICAR, OUTCAR, etc)
		
		print "Found",len(base_list),"incomplete jobs"
		
		total_failed += len(base_list)
		
		# Delete corresponding .OUTCAR files
		
		for j in xrange(len(base_list)):
			helpers.run_bash_cmnd("rm -f " + base_list[j] + ".OUTCAR")
			
		# Update the *.INCAR files for the cases
		
		print helpers.run_bash_cmnd("pwd")
		
		incars = None
		
		for j in xrange(args_cases):
			incars = glob.glob("CASE-" + `j` + "/*.INCAR")
			
		for j in xrange(len(incars)):
			
			print "Working on:",incars[j]
			
			hepers.run_bash_cmnd("cp " + incars[j] + " " + incars[j] + ".bck")
		
			contents = helpers.readlines(incars[j])
			
			# Get index of line containing "IALGO"
			
			targ = next(i for i, w in enumerate(contents) if "IALGO" in w)
			line = contents[targ].split()
			
			# Make sure it contains the expected value
			
			if int(line[2]) != 48:
				print "ERROR: Expeted IALGO = 48, got",line[2]
				print "Would have replaced with 38"
				exit()
				
			# Replace with 38, write to file
			
			line[2] = "38"
			contents[targ] = ' '.join(line)+'\n'
	
			helpers.writelines(incars[j],contents)
			
			print "\tFile",incars[j],"updated"

		os.chdir("..")
	os.chdir("..")
	
	return total_failed

		
		
				
			
			
					
os.chdir("/p/lustre2/rlindsey/DNTF_MODEL-3")
check_convergence(3,7,["all"])

# NOTE: vasp_driver.continue_job counts #.POSCARS and #.OUTCARS ... if !=, then simply resubs the .cmd file and lets the .cmd file take care of the rest of the logic
# The .cmd file also looks to see if *.OUTCAR existis... if it does, it skips the job. otherwise, copies <temperature>.incar to incar and builds the corresponding potcar
#
# So what we'd need to do is delete the corresponding .OUTCARS, and then edit all .INCAR's to have IALGO = 38		

