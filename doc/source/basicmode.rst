***************************************
Basic Fitting Mode
***************************************


.. figure:: ALD_workflow.pdf
  :width: 600
  :align: center
  
  **Fig. 1:** The ChIMES Active Learning Driver Workflow.

Despite its name, the ALD can be run without any active learning. For simplicity this documentation will describe all other features as they are executed in this basic mode. Active learning features are described in **SECTION**, and **SECTION** provides an option compatibility table. 

-------

============================
Setting up Steps 1 & 2
============================

As with a standard ChIMES fit (see e.g, LINK TO LSQ DOCS), model generation must begin selecting an intial training set and specifying fitting hyperparameters. In the ALD, this involves the following files, at a minimum:

.. code-block :: text

    <my_fit>/ALL_BASE_FILES/ALC-0_BASEFILES/fm_setup.in
    <my_fit>/ALL_BASE_FILES/ALC-0_BASEFILES/traj_list.dat
    <my_fit>/ALL_BASE_FILES/ALC-0_BASEFILES/*xyzf
    <my_fit>/config.py

The ``fm_setup.in`` file is created as usual, except:
* The ``# TRJFILE #`` option should be set to ``MULTI traj_list.dat``, and 
* The ``# SPLITFI #`` option should be set to ``false``.
See LINK TO LSQ DOCS for more information on what these settings control.

The ``traj_list.dat`` file should be structured as usual for ChIMES LSQ, but lines containing the first n-cases entries should have a temperature in Kelvin specified at the very end, where n-cases is the number of statepoints the user would like to simultaneously conduct iterative training to:

.. code-block :: text

    3
    10 1000K_1.0gcc.xyzf 1000
    10 2000K_2.0gcc.xyzf 2000
    10 3000K_3.5gcc.xyzf 3000
    
Note that the above .xyzf files correspond to <my_fit>/ALL_BASE_FILES/ALC-0_BASEFILES/*xyzf.
    

        
Finally, options for this first phase of fitting ``config.py`` must be specified. PAGE provides a complete set of options and details default values. Note that for this basic overview we will assume:

* The user is running on a SLURM/SBATCH based HPC system,
* The HPC system has 36 processors per compute node, and 
* We want to generate hydrogen parameters by iteratively fitting at 3 statepoints, in simultaneously (**indicated by line 6**).


The minimal config.py lines necessary for steps 1 & 2 are provided in the code block below. Recalling that ALD functions primarily as a workflow tool, it must be linked with external software. Here, we tell the ALD:

* Where the ALD source code is located (line 8),
* Where the ALD will be run (line 9), and 
* Where to find our ChIMES_LSQ installation (line 10). 

Lines 16-19 tell the ALD where all the files needed to run chimes_lsq are, specifically:

* The ChIMES LSQ input files, fm_setup.in and traj_list.dat (line 16),
* The ChIMES LSQ design matrix generation executable, chimes_lsq  (line 17),
* The ChIMES LSQ matrix solution script, chimes_lsq.py (line 18), and 
* The ChIMES LSQ parameter file scrubber, post_proc_lsq2.py (line 19).

Finally, lines 23-25 specify how forces, energies, and stresses should be weighted, while lines 27-29 specify how the matrix solution problem should be executed, i.e., using distributed lasso (line 27) with a regularization variable of 1e-8 (line 28), and with a normalized design matrix (line 29).


.. code-block :: text
    :linenos:

    ################################
    ##### General options
    ################################

    ATOM_TYPES     = ["H"]
    NO_CASES       = 3

    DRIVER_DIR     = "/path/to/active_learning_driver/src"
    WORKING_DIR    = "/path/to/directory/where/learning/will/occur"
    CHIMES_SRCDIR  = "/path/to/chimes_lsq/installation/src"

    ################################
    ##### ChIMES LSQ
    ################################

    ALC0_FILES    = WORKING_DIR + "ALL_BASE_FILES/ALC-0_BASEFILES/"
    CHIMES_LSQ    = CHIMES_SRCDIR + "chimes_lsq"
    CHIMES_SOLVER = CHIMES_SRCDIR + "lsq2.py"
    CHIMES_POSTPRC= CHIMES_SRCDIR + "post_proc_lsq2.py"

    # Generic weight settings

    WEIGHTS_FORCE =   1.0s
    WEIGHTS_ENER  =   0.1
    WEIGHTS_STRES = 100.0

    REGRESS_ALG   = "dlasso"
    REGRESS_VAR   = "1.0E-8"
    REGRESS_NRM   = True
    

-------


============================
Setting up Step 3
============================

Step 3 comprises molecular dynamics (MD) simulation with the parameters generated in step 2. Beyond the parameter file, this requires the following at a minimum:


* An initial coordinate file,
* A MD input file specifying the simulation style,
* A MD code executable, and 
* Instructions on how to post-process resultant trajectories

Recalling that the current example concerns concurrent iterative fitting for three cases (training state points), the is specified by the following in ``../../ALL_BASE_FILES/CHIMESMD_BASEFILES/`` and ``config.py``, i.e.:

.. code-block :: text

    <my_fit>/ALL_BASE_FILES/CHIMESMD_BASEFILES/case-0.indep-0.input.xyz
    <my_fit>/ALL_BASE_FILES/CHIMESMD_BASEFILES/case-0.indep-0.run_md.in
    <my_fit>/ALL_BASE_FILES/CHIMESMD_BASEFILES/case-1.indep-0.input.xyz
    <my_fit>/ALL_BASE_FILES/CHIMESMD_BASEFILES/case-1.indep-0.run_md.in
    <my_fit>/ALL_BASE_FILES/CHIMESMD_BASEFILES/case-2.indep-0.input.xyz
    <my_fit>/ALL_BASE_FILES/CHIMESMD_BASEFILES/case-2.indep-0.run_md.in
    <my_fit>/ALL_BASE_FILES/CHIMESMD_BASEFILES/bonds.dat
 
and 

.. code-block :: text
    :linenos:

    ################################
    ##### Molecular Dynamics
    ################################

    MD_STYLE        = "CHIMES"
    CHIMES_MD_MPI   = CHIMES_SRCDIR + "chimes_md-mpi"

    MOLANAL         = "/path/to/molanlal/folder/"
    MOLANAL_SPECIES = ["H1", "H2 1(H-H)", "H3 2(H-H)"]


Each ``case-*.indep-0.input.xyz`` is a ChIMES ``.xyz`` file containing initial coordinates for the system of interest for the corresponding case, while each ``case-*.indep-0.run_md.in`` is the corresponding ChIMES MD input file. Note that ``case-*.indep-0.run_md.in`` options ``# PRMFILE #`` and ``# CRDFILE #`` should be set to ``WILL_AUTO_UPDATE``. The bonds.dat file will be described below.

In the config.py file, lines 5-7 tell the ALD to use ChIMES MD for MD simulation runs, and provides a path to the MPI-enabled and serial compilations. Lines 9 and 10 provide information on how to post-process the trajectory. Specifically, the ALD will use the a molecular analyzer (molanal) REFERENCE LARRYS PAPER to determine speciation for the generated MD trajectories. Once speciation is determined, the ALD will provide a summary of lifetimes and molefractions for species listed in ``MOLANAL_SPECIES``. Note that the species names must match the "Molecule type" fields produced by molanal *exactly*. These strings are usually determined by running molanal on DFT-MD trajectories, prior to any ALD. Finally, the ``bonds.dat`` file specifies bond length and lifetime criteria for molanal. See the molanal ``readme.txt`` file for additional information. Be sure to verify specified bonds.dat lifetime criteria are consistent with the timestep and output frequency specified in ``case-*.indep-0.run_md.in``

-------

============================
Setting up Step 4
============================

Model validation is purposefully left to the user, as optimal strategies are still an active area of research. The user is encouraged to investigate fit performance and physical property recovery on their own. For additional discussion, see SECTION

-------

============================
Setting up Step 5
============================

Candidate configuration filtering is conducted in step 5. For basic fitting mode, this simply comprises selecting a subset of configuratiosn generated during the previous MD step for single point evaluation using, e.g., DFT. This is handled entirely automatically by the ALD.

-------

============================
Setting up Step 6
============================

Step 6 comprises single point evaluation of configurations selected in step 5 via the user's requested quantum-based reference method. In this overview, we will assume the user is employing VASP. To do so, the following must be provided, at a minimum:

.. code-block :: text

    <my_fit>/ALL_BASE_FILES/QM_BASEFILES/*.INCAR
    <my_fit>/ALL_BASE_FILES/QM_BASEFILES/KPOINTS
    <my_fit>/ALL_BASE_FILES/QM_BASEFILES/*.POTCAR

and

.. code-block :: text

    ################################
    ##### Single-Point QM
    ################################
    
    QM_FILES = WORKING_DIR + "ALL_BASE_FILES/QM_BASEFILES"
    VASP_EXE = "/path/to/vasp/executable"
    
    
There should be one ``*.INCAR`` file for each case temperature, i.e. ``{1000,2000,3000}.INCAR`` for the present example, with all options set to user desired values for single point evaluation. Note that ``IALGO = 48`` should be used to specifiy the electronic minimisation algorithm, and any variable related to restart should be set to the corresponding "new" value. There should also be one ``.*POTCAR`` file for each atom type considered, i.e. H.POTCAR for the present example.



