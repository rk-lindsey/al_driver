#######################################
Quick Start
#######################################

.. Note :: 

    The ALD is currently written in python2.7. An updrade to 3.8 is (probably) coming soon.


=========================
System Configuration
=========================

The ALD **must** be run on an HPC platform and it currently only supports SLURM/SBATCH systems. 


.. Tip :: 

    The ALD is trivially extendable to other queuing sytems for all running modes except cluster-based active learning, and can be run without  cluster-based active learning support. For basic extension, add a conditional statement to ``helpers.create_and_launch_job``, i.e.:
    
    .. code-block :: python
    
        if args["job_system"] == "slurm":
        
            # Do what is currently implemented
        
        elif args["job_system"] == "your_new_scheduler_name":
        
            # Use current implementation as template and modify for your scheduler
            
        else:
        
            print "ERROR: Unrecognized scheduler: ", args["job_system"]
            exit()
    
    and make similar edits to ``helpers.wait_for_job`` and ``helpers.wait_for_jobs``. Search for "srun" in ``*.py`` files to check for compatibility with your system. When running, set ``HPC_SYSTEM=your_new_scheduler_name``


    To add support for cluster-based active learning, additional ``utilities/new*sh`` files will need to be added and property selected for in ``cluster.py``



=========================
ChIMES LSQ and ChIMES MD
=========================

The ALD **requires** the ChIMES LSQ/MD code, verseion VERSION. A copy can be downloaded HERE. Two compilations will be needed: Serial and MPI-supported. These compilations can be generated via:

.. code-block :: bash

    code to compile two different versions of chimes_lsq and chimes_md
    
The molanal utility will also be required and can be compiled via:

.. code-block :: bash


    code to compile molanal

If the above instructions are followed properly, the following executables/scripts should be generated:

* chimes_lsq
* chimes_md-serial
* chimes_md-mpi
* chimes_lsq.py
* post_process_lsq2.py
* dlars
* molanal/{executables}

-----

=========================
Reference Methods
=========================

The ALD currently supports VASP and DFTB+ for data lableing (i.e. providing forces, energies, and stresses for configurations) in periodic system and Gaussian for non-periodic systems. Current implmentations are configured for the following software versions:

* VASP 5.4.1
* Gaussian 16
* DFTB+ 17.1

Support for newer DFTB+ versions is in progress. 

Future efforts will also focus on supporting LAMMPS as a datalabeling method, allowing, e.g., coarse-grained model development based on molecular mechanics potentials. 

-----

=========================
Correction Support
=========================

The ALD currently supports generating ChIMES corrections for DFTB via DFTB+, however it currently requires an in-house compilation. Support via DFTB+/the ChIMES calculator is under development.

