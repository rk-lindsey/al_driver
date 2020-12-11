# Global (python) modules

import os
import sys

# Local modules

import helpers
import gen_ff
import run_md
import cluster
import gen_selections
import qm_driver
import restart

# Allow config file to be read from local directory

local_path = os.path.normpath(helpers.run_bash_cmnd("pwd").rstrip())
sys.path.append(local_path)
import config  # User-specified "global" vars


def main(args):



	################################
	# Initialize vars
	################################

	THIS_CASE  = 0
	THIS_INDEP = 0
	EMAIL_ADD  = ''
	SMEARING   = "TRAJ_LIST"
	
	if os.path.normpath(config.WORKING_DIR) != local_path:
	
		print "Error: this script was not run from config.WORKING_DIR!"
		print "config.WORKING_DIR:",config.WORKING_DIR
		print "local path:        ",local_path
		print "Exiting."
		
		exit()
	
	print "The following has been set as the working directory:"
	print '\t', config.WORKING_DIR
	print "The ALC-X contents of this directory will be overwritten."

	################################
	# Pre-process user specified variables
	################################

	config.ATOM_TYPES.sort()

	config.CHIMES_SOLVER  = config.HPC_PYTHON + " " + config.CHIMES_SOLVER
	config.CHIMES_POSTPRC = config.HPC_PYTHON + " " + config.CHIMES_POSTPRC

	config.VASP_POSTPRC   = config.HPC_PYTHON + " " + config.VASP_POSTPRC
	config.GAUS_POSTPRC   = config.HPC_PYTHON + " " + config.GAUS_POSTPRC
	
	if config.EMAIL_ADD:
		EMAIL_ADD = config.EMAIL_ADD	
		
	if config.THIS_SMEAR:
		SMEARING = config.THIS_SMEAR

		print "Will use a smearing temperature of",SMEARING,"K"
	else:
		print "Will read smearing temperatures from traj_list.dat file"	

	################################
	################################
	# Begin Active Learning
	################################
	################################

	print "Will run for the following active learning cycles:"

	ALC_LIST = args

	for THIS_ALC in ALC_LIST:
		print THIS_ALC
		

	# Set up the restart file
		
	restart_controller = restart.restart() # Reads/creates restart file. Must be named "restart.dat"

	ALC_LIST = restart_controller.update_ALC_list(ALC_LIST)

	print "After processing restart file, will run for the following active learning cycles:"

	for THIS_ALC in ALC_LIST:
		print THIS_ALC
		
	if type(config.USE_AL_STRS) is int:
		print "Will include stress tensors for self-consistently obtained full-frames, for ALC >=",config.USE_AL_STRS
	
	else:
		config.USE_AL_STRS = ALC_LIST[-1]+1 # Set to one greater than the number of requested ALCs


	for THIS_ALC in ALC_LIST:

		THIS_ALC = int(THIS_ALC)
		
		
		# Let the ALC process know whether this is a restarted cycle or a completely new cycle
		
		if THIS_ALC != restart_controller.last_ALC:
		
			restart_controller.reinit_vars()
		
		
		# Prepare the restart file

		restart_controller.update_file("ALC: " + str(THIS_ALC) + '\n')
			

		print "Working on ALC:", THIS_ALC

		os.chdir(config.WORKING_DIR)
		

		# Begins in the working directory (WORKING_DIR)

		if THIS_ALC == 0: # Then this is the first ALC, so we need to do things a bit differently ... 
		
		
			if not restart_controller.BUILD_AMAT: # Then we haven't even begun this ALC

				# Set up/move into the ALC directory
			
				helpers.run_bash_cmnd("rm -rf ALC-" + str(THIS_ALC))
				helpers.run_bash_cmnd("mkdir  ALC-" + str(THIS_ALC))
			
			os.chdir("ALC-" + str(THIS_ALC))
			
					
			################################
			# Generate the force field	
			################################
			
			if not restart_controller.BUILD_AMAT:
			
				# Note: Stress tensor inclusion controlled by contents of config.ALC0_FILES
			
				active_job = gen_ff.build_amat()


				active_job = gen_ff.solve_amat()	
				
...at this point we already have a ff based on the QM FF
			################################				
			# Extract/process/select clusters
			################################
			
if do_cluster and 			if not restart_controller.CLUSTER_EXTRACTION:

				# Get a list of files from which to extract clusters
			
				traj_files = helpers.cat_to_var("GEN_FF/traj_list.dat")[1:]
			
				# Extract clusters from each file, save into own repo, list

				for i in xrange(len(traj_files)):

					# Extract
			
					cluster.generate_clusters()

					# list
					
					cluster.list_clusters(repo, config.ATOM_TYPES, config.MAX_CLUATM)

if do_cluster and 			if not restart_controller.CLUENER_CALC:

				# Compute cluster energies
			
				active_jobs = cluster.get_repo_energies()	
			
			
if do_cluster and 			if not restart_controller.CLU_SELECTION:
			
				# Generate cluster sub-selection and store in central repository

				gen_selections.gen_subset() # Seed for random number generator	
			
				gen_selections.populate_repo(THIS_ALC)


			################################
			# Launch QM Cluster calculations
			################################

if do_cluster and 			if not restart_controller.INIT_QMJOB:	
	
				qm_driver.cleanup_and_setup(config.BULK_QM_METHOD, config.IGAS_QM_METHOD, ["all"], build_dir=".") # Always clean up, just in case	

				
if do_cluster and 			if not restart_controller.THIS_ALC:

				# Post-process the qm jobs

				qm_driver.post_process()

			os.chdir("..")
			
			print "ALC-", THIS_ALC, "is complete"	
# CONCLUDE ALC-0
		else:
# START ALL OTHER ALCC's


		
and do_cluster			if not restart_controller.BUILD_AMAT: # Then we haven't even begun this ALC
	
			
				active_job = gen_ff.build_amat(THIS_ALC, 
					prev_qm_all_path = qm_all_path,
					prev_qm_20_path  = qm_20F_path,
					include_stress     = do_stress,	
					stress_style       = config.STRS_STYLE,
					job_email          = config.HPC_EMAIL,
					job_ppn            = str(config.HPC_PPN),
					job_nodes          = config.CHIMES_BUILD_NODES,
					job_walltime       = config.CHIMES_BUILD_TIME,	
					job_queue          = config.CHIMES_BUILD_QUEUE,						
					job_account        = config.HPC_ACCOUNT, 
					job_system         = config.HPC_SYSTEM,
					job_executable     = config.CHIMES_LSQ)

						
				
and do_cluster			if not restart_controller.SOLVE_AMAT:	
			
				active_job = gen_ff.solve_amat()	
						
					helpers.wait_for_job(active_job, job_system = config.HPC_SYSTEM, verbose = True, job_name = "solve_amat")

if not do_cluster

	then copy A_comb.txt b_comb.txt b-labeled_comb.txt params.txt force.txt....... and maybe also weights from alc-0's GEN_FF to ALC_1's
				
			################################				
			# Run MD
			################################
			
			
			if not restart_controller.RUN_MD:
	
				for THIS_CASE in xrange(config.NO_CASES):

					active_job = run_md.run_md()

			if not restart_controller.POST_PROC:
			
				for THIS_CASE in xrange(config.NO_CASES):	
			
					# Post-process the MD job
			
					run_md.post_proc()

if do_cluster		if not restart_controller.CLUSTER_EXTRACTION:
			

				for THIS_CASE in xrange(config.NO_CASES):
				        
				        cluster.list_clusters(repo, config.ATOM_TYPES, config.MAX_CLUATM)
					
if do_cluster		if not restart_controller.CLUENER_CALC:
			
				# Compute cluster energies
			
				gen_selections.cleanup_repo(THIS_ALC)	
			
				active_jobs = cluster.get_repo_energies()	
	
if do_cluster		if not restart_controller.CLU_SELECTION:

				# Generate cluster sub-selection and store in central repository

				gen_selections.gen_subset() # Maximum energy to consider	
						 
				gen_selections.populate_repo(THIS_ALC)   
						 			 

			################################
			# Launch QM
			################################
			
			# Note: If multiple cases are being used, only run clean/setup once!
			
				
			if not restart_controller.INIT_QMJOB:	

				for THIS_CASE in xrange(config.NO_CASES):

if do_cluster ... otherwise change this call	qm_driver  .cleanup_and_setup(config.BULK_QM_METHOD, config.IGAS_QM_METHOD,["20", "all"], THIS_CASE, build_dir=".") # Always clean up, just in case
										
					active_job = qm_driver.setup_qm()

						
			if not restart_controller.THIS_ALC:

				# Post-process the vasp jobs

again, change this call based on do_cluster				qm_driver.post_process()				
						
						
			os.chdir("..")
			
			print "ALC-", THIS_ALC, "is complete"	
			
			restart_controller.update_file("THIS_ALC: COMPLETE" + '\n')	

			print helpers.email_user(config.DRIVER_DIR, EMAIL_ADD, "ALC-" + str(THIS_ALC) + " status: " + "THIS_ALC: COMPLETE ")
					

if __name__=='__main__':

	""" 
	
	Allows commandline calls to main().
	
	      	
	"""	
	
	main(sys.argv[1:])
