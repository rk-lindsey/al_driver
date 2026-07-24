.. _page-quickstart:

#######################################
Quick Start
#######################################

The ALD is a workflow tool that autonomously generates ChIMES models by orchestrating, running, and monitoring the various different tasks involved in iteratively learning a model. By necessity, this involves generating input for, using, and post-processing output from several codes, download and installation of which are described in the following sections. 

.. Note ::

    System requirements for the ALD include: 


    * An HPC platform with job queueing - currently supports SLURM/SBATCH-based (slurm, conda-slurm, TACC, UM-ARC) and torque/PBS systems
    * C, C++11, and Fortran 77, 90, and 08 compilers
    * MPI compilers
    * MKL
    * Python version 3

    Note that the ALD is trivially extendable to other queuing systems for all running modes except cluster-based active learning, and can be run without  cluster-based active learning support. See the :ref:`page-extending` page for additional details. 
    
    

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

    If you are not running on an LLNL (Quartz), UM (Great Lakes), or TACC (Stampede3) system, you will need to manually configure your compilers. We recommend Intel OneAPI, which is freely available. You will need to compile dlars and molanal by hand (see install script for steps).
    

.. Warning :: 

    The installation command will only work if the appropriate modules are loaded and the user has specified the hosttype. 
    To specify hosttype, run `export hosttype=<machine name>`. For further information, refer to `ChIMES LSQ Documentation <https://chimes-lsq.readthedocs.io/en/latest/>`_.
    

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

The ALD currently supports VASP, DFTB+, CP2K, and LAMMPS for data labeling (i.e. providing forces, energies, and stresses for configurations) in periodic systems and Gaussian for non-periodic systems. Current implementations are configured for the following software versions:

* VASP 5.4.1 or later (`link <https://www.vasp.at>`_)
* Gaussian 16 (`link <https://gaussian.com/gaussian16/>`_)
* DFTB+ 25.1 (`link <https://github.com/dftbplus/dftbplus>`_); ChIMES-corrected DFTB verified against development commit 6ae315b4
* CP2K 2022.2 (`link <https://github.com/cp2k/cp2k/releases/tag/v2022.2>`_)
* LAMMPS/29Aug2024(`link <https://github.com/lammps/lammps/tree/stable_29Aug2024_update1>`_)

.. Note ::

   ALD compiled with these software versions are guaranteed to run. Support for newer versions is being evaluated; compatibility is not guaranteed.

-----

==================================================
Note on Correction Support
==================================================

The ALD supports generating ChIMES corrections for DFTB via DFTB+ compiled with ChIMES calculator support (see the `DFTB+ Recipes <https://dftbplus-recipes.readthedocs.io/en/stable/>`_). An in-house DFTB+ compilation is no longer required. See the :ref:`page-correction` page for a worked example.

