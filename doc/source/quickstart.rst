.. _page-quickstart:

#######################################
Quick Start
#######################################

The ALD is a workflow tool that autonomously generates ChIMES models by orchestrating, running, and monitoring the various different tasks involved in iterative learning a model. By necessity, this involves generating input for, using, and post-processing output from several codes, download and installation of which are described in the following sections. 

.. Note ::

    System requirements for the ALD include: 


    * An HPC platform with job queueing - currently support SLURM/SBATCH and PBS/qsub systems
    * C, C++11, and Fortran 77, 90, and 08 compilers
    * MPI compilers
    * MKL
    * Python version 3

    Note that the ALD is trivially extendable to other queuing sytems for all running modes except cluster-based active learning, and can be run without  cluster-based active learning support. See the "**<EXTENDING>**" page for additional details. 
    
    

==================================================
Installing ChIMES LSQ and ChIMES MD
==================================================

The ALD requires a specific version of the ChIMES LSQ/MD code. To download and compile it, log into your HPC system, execute the following commands, and agree to all prompted questions:

.. code-block :: bash

    cd /path/to/my/software/folder
    mkdir chimes_lsq-forALD
    git clone https://github.com/rk-lindsey/chimes_lsq.git chimes_lsq-forALD
    cd chimes_lsq-forALD
    ./install.sh

.. Warning :: 

    If you are note running on an LLNL (Quartz), UM (Great Lakes), or TACC (Stampede3) system, you will need to manually configure your compilers. We recommend Intel OneAPI, which is freely available. You will need to compile dlars and molanal by hand (see install script for steps).
    

.. Warning :: 

    The installation command will only work if the appropriate modules are loaded and the user has specified the hosttype. 
    To specify hosttype, run `export hosttype=<machine name>`. For further infomation, refer to `ChIMES LSQ Documentation <https://chimes-lsq.readthedocs.io/en/latest/>`_.
    

If the above instructions are followed properly, the following executables/scripts should be generated:

.. code-block :: bash

    ./build/chimes_lsq
    ./build/chimes_md-serial 
    ./build/chimes_md-mpi
    ./build/chimes_lsq.py
    ./build/post_proc_chimes_lsq.py
    ./contrib/dlars/src/dlars
    ./contrib/molanal/src/molanal.new

-----

=============================================================
Installing Reference (Data Labeling) Methods
=============================================================

The ALD currently supports VASP, DFTB+, CP2K, and LAMMPS for data lableing (i.e. providing forces, energies, and stresses for configurations) in periodic system and Gaussian for non-periodic systems. Current implmentations are configured for the following software versions:

* VASP 5.4.1 or later(`link <https://www.vasp.at>`_)
* Gaussian 16 (`link <https://gaussian.com/gaussian16/>`_)
* DFTB+ 17.1 (`link <https://github.com/dftbplus/dftbplus/releases/tag/17.1>`_)
* CP2K 2022.2 (`link <https://github.com/cp2k/cp2k/releases/tag/v2022.2>`_)
* LAMMPS/29Oct2020 (`link <https://download.lammps.org/tars/index.html>`_)

.. Note ::

   ALD compiled with these software versions are guaranteed to run. However, we are unable to confirm its compatibilities with later versions. Support for newer versions of these softwares is in progress.

-----

==================================================
Note on Correction Support
==================================================

The ALD currently supports generating ChIMES corrections for DFTB via DFTB+, however it requires an in-house compilation. Support via DFTB+/the ChIMES calculator is under development.

