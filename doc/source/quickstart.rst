.. _page-quickstart:

#######################################
Quick Start
#######################################

The ALD is a workflow tool that autonomously generates ChIMES models by orchestrating, running, and monitoring the various different tasks involved in iterative learning a model. By necessity, this involves generating input for, using, and post-processing output from several codes, download and installation of which are described in the following sections. 

.. Note ::

    System requirements for the ALD include: 


    * An HPC platform with job queueing - currently only SLURM/SBATCH systems are supported
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

    If you are note running on an LLNL (Quartz) or UM (Great Lakes) system, you will need to manually configure your compilers. We recommend Intel OneAPI, which is freely available. You will need to compile dlars and molanal by hand (see install script for steps).
    
 
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

The ALD currently supports VASP and DFTB+ for data lableing (i.e. providing forces, energies, and stresses for configurations) in periodic system and Gaussian for non-periodic systems. Current implmentations are configured for the following software versions:

* VASP 5.4.1 (`link <https://www.vasp.at>`_)
* Gaussian 16 (`link <https://gaussian.com/gaussian16/>`_)
* DFTB+ 17.1 (`link <https://dftbplus.org/download/deprecated/dftb-171>`_)

Support for newer VASP and DFTB+ versions is in progress. Future efforts will also focus on supporting LAMMPS as a data labeling method, allowing, e.g., coarse-grained model development based on molecular mechanics potentials. 

-----

==================================================
Note on Correction Support
==================================================

The ALD currently supports generating ChIMES corrections for DFTB via DFTB+, however it requires an in-house compilation. Support via DFTB+/the ChIMES calculator is under development.

