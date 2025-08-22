.. _page-extending:


#######################################
Extending the ALD
#######################################


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

===================
Adding a new labeling method
===================

To add a new labeling method, edit the following scripts:

- ``main.py``
- ``qm_driver.py``
- ``verify_config.py``

Additionally, create a new Python script to be read by ``qm_driver.py`` to perform the relabeling. Follow the same code structure as existing ``*_driver.py`` scripts e.g. ``vasp_driver.py``. Update ``verify_config.py`` and ``main.py`` so that your new driver's required variables are defined, briefly explained, and assigned default values.

To commit the changes, you must provide a minimum working example using your labeling method and a successful run through the current example list for acceptance.

===================
Adding a new MD method
===================

To add a new MD method, edit the following scripts:

- ``main.py``
- ``run_md.py``
- ``verify_config.py``

Create a new Python script to be read by ``run_md.py`` to perform the MD. Follow the same code structure as other ``*_run_md.py`` scripts. Update ``verify_config.py`` and ``main.py`` so that all required variables for your new driver are defined, briefly explained, and assigned default values.

To commit the changes, provide a minimum working example using your MD method and ensure it passes the current example list.