.. _page-extending:


#######################################
Extending the ALD
#######################################

UNDER CONSTRUCTION



------


     For basic extension, add a conditional statement to ``helpers.create_and_launch_job``, i.e.:
     
     .. code-block :: python
     
         if args["job_system"] == "slurm":
         
             # Do what is currently implemented
         
         elif args["job_system"] == "your_new_scheduler_name":
         
             # Use current implementation as template and modify for your scheduler
             
         else:
         
             print "ERROR: Unrecognized scheduler: ", args["job_system"]
             exit()
     
     and make similar edits to ``helpers.wait_for_job`` and ``helpers.wait_for_jobs``. Search for "srun" in ``*.py`` files to check for compatibility with your system. When running, set ``HPC_SYSTEM=your_new_scheduler_name``
 
 
     To add support for cluster-based active learning, additional ``utilities/new*sh`` files will need to be added and properly selected for in ``cluster.py``


