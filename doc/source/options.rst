

.. _page-basic:

########################################################
ChIMES Active Learning Driver Configuration File Options
########################################################

***************************************
Optional config.py Variables:
***************************************

========================
Assorted General Options
========================

=======================   ===============  ======== ====================   ============================
Input variable            Variable type    Required Default                Value/Options/Notes
=======================   ===============  ======== ====================   ============================
``EMAIL_ADD       =``     str              N        ""                     E-mail address for driver to sent status updates to. If blank (""), no emails are sent.
``SEED            =``     int              N        1                      Only used for active learning strategies are selected. Seed for random number generator.
``ATOM_TYPES      =``     list of str      Y        None                   List of atom types in system of interest, e.g. ["C","H","O"].
``NO_CASES        =``     int              Y        None                   Number of different state points at which to conduct iterative learning.
``MOLANAL_SPECIES =``     list of str      N        [""]                   List of species to track in molanal output, e.g. [\"C1 O1 1(O-C)\", \"C1 O2 2(O-C)\"].
``USE_AL_STRS     =``     int              N        0                      Cycle at which to start including stress tensors from ALC generated configrations.
``STRS_STYLE      =``     str              N        "ALL"                  How stress tensors should be included in the fit. Options are: "DIAG" or "ALL".
``THIS_SMEAR      =``     int              N        float                  Thermal smearing temperature in K; if \"None\", different values are used for each case, set in the ALL_BASE_FILES traj_list.dat.
``DRIVER_DIR      =``     str              Y        None                   Location of the source directory for ALD
``WORKING_DIR      =``    str              Y        None                   Location of the ALD job being ran
=======================   ===============  ======== ====================   ============================

===================
General HPC Options
===================

==================  =============  ========== ====================    ============================
Input variable      Variable type  Required   Default                 Value/Options/Notes
==================  =============  ========== ====================    ============================
``HPC_PPN     =``   int            Y          36                      Number of processors per node on HPC platform.
``HPC_ACCOUNT =``   str            Y          None                    Charge bank/account name on HPC platform.
``HPC_SYSTEM  =``   str            N          slurm                   HPC platform type options are slurm, TACC, or qsub.
``HPC_PYTHON  =``   str            Y          None                    Full path to python2.X exectuable on HPC platform.
``HPC_EMAIL   =``   bool           N          True                    Controls whether driver status updates are e-mailed to user.
==================  =============  ========== ====================    ============================


==========================
ChIMES LSQ  Options
==========================

========================    =============  ======== ======================================================================      ============================
Input variable              Variable type  Required Default                                                                     Value/Options/Notes
========================    =============  ======== ======================================================================      ============================
``ALC0_FILES         =``    str            N        ``WORKING_DIR`` + "ALL_BASE_FILES/ALC-0_BASEFILES/"                         Path to LSQ base files required by the driver (e.g. traj_list.dat, fm_setup.in, etc.)-Note: In greatlakes, all paths provided must be absolute paths using the "realpath" command, not just the current working directory from "pwd".
``CHIMES_LSQ         =``    str            Y        ``CHIMES_SRCDIR`` + "chimes_lsq"                                            Absolute path to ChIMES_lsq executable.
``CHIMES_LSQ_MODULES =``    str            Y        "cmake/3.21.1 + mkl + intel-classic/2021.6.0-magic + mvapich2/2.3.7"        System-specific modules needed to run ChIMES-LSQ jobs
``CHIMES_SOLVER      =``    str            N        ``CHIMES_SRCDIR`` + "lsq2.py"                                               Absolute path to ChIMES_lsq.py (formely, lsq2.py).
``CHIMES_POSTPRC     =``    str            N        ``CHIMES_SRCDIR`` + "post_proc_lsq2.py"                                     Absolute path to post_proc_lsq2.py.
``CHIMES_SRCDIR	     =``    str            Y        ""                                                                          Path to directory containing the ChIMES_LSQ source code        
``CHIMES_BUILD_NODES =``    int            Y        4                                                                           Number of nodes to use when running chimes_lsq.
``CHIMES_BUILD_QUEUE =``    str            Y        pbatch                                                                      Queue to submit chimes_lsq job to.
``CHIMES_BUILD_TIME  =``    str            Y        "04:00:00"                                                                  Walltime for chimes_lsq job.
``CHIMES_SOLVE_NODES =``    int            Y        8                                                                           Number of nodes to use when running dlasso
``CHIMES_SOLVE_PPN   =``    int            Y        ``HPC_PPN``                                                                 Number of procs per node to use when running dlasso
``CHIMES_SOLVE_QUEUE =``    str            Y        pbatch                                                                      Queue to submit the dlasso job to
``CHIMES_SOLVE_TIME  =``    str            Y        "04:00:00"                                                                  Walltime for dlasso job
``N_HYPER_SETS  =``         int            N        1                                                                           Number of unique fm_setup.in files; allows fitting, e.g., multiple overlapping models to the same data
``REGRESS_ALG        =``    str            N        dlasso                                                                      Regression algorithm to use for fitting; only dlasso supported for now
``REGRESS_VAR        =``    float          N        1e-5                                                                        Regression regularization variable.
``REGRESS_NRM        =``    bool           N        True                                                                        Controls whether A-matrix is normalized prior to solution.
``WEIGHTS_SET_ALC_0  =``    bool           N        False                                                                       Should ALC-0 (or 1 if no clustering) weights be read directly from a user specified file?
``WEIGHTS_ALC_0      =``    str            N        None                                                                        Set if ``WEIGHTS_SET_ALC_0`` is true; path to user specified ALC-0 (or ALC-1) weights.
``WEIGHTS_FORCE      =``    special        N        1.0                                                                         Weights to apply to full-frame forces - many options, see note below.
``WEIGHTS_FGAS       =``    special        N        5.0                                                                         Weights to apply to gas phase forces - many options, see note below.
``WEIGHTS_ENER       =``    special        N        0.1                                                                         Weights to apply to full-frame energies - many options, see note below.
``WEIGHTS_EGAS       =``    special        N        0.1                                                                         Weights to apply to gas phase energies - many options, see note below.
``WEIGHTS_STRES      =``    special        N        250.0                                                                       Weights to apply to full-frame stress tensor components - many options, see note below.
========================    =============  ======== ======================================================================      ============================

.. Note ::

    There are numerous options available for weighting, and weights are applied separately to full-frame forces, gas phase forces, full-frame energies, gas phase energies, and full-frame  stress. 
    
    If a ``WEIGHTS_*`` option is set to a single floating point value, that value is applied to all candidate data of that type, e.g., if ``WEIGHTS_FORCE`` = 1.0, all full-frame forces will be assigned a weight of 1.0. 
    
    Additional weighting styles can be selected by letter:

	``A`` w = a0
	
	``B`` w = a0*(this_cycle-1)^a1         # NOTE: treats this_cycle = 0 as this_cycle = 1
	
	``C`` w = a0*exp(a1*|X|/a2)
	
	``D`` w = a0*exp(a1[X-a2]/a3)
	
	``E`` w = n_atoms^a0
         
        ``F`` w = a0*exp(a1[ X/n_atoms-a2]/a3)
    
        ``G`` w = a0*exp(a1(|X|-a2)/a3)
    
    where "X" is the value being weighted.
    
    ``WEIGHTS_FORCE = [["B"],[1.0,-1.0]]`` would select weighting style B and apply a weight of 1.0 to each full-frame force component in the first ALD cycle; weighting would decrease by a factor (this_cycle)^(-1.0) each cycle. 
    
    Multiple weighting schemes can be combined as well. For example ``WEIGHTS_FORCE = [ ["A","B"], [[100.0  ],[1.0,-1.0]]]`` would add an additional multiplicative factor of 100 to the previous example. 
	
==========================
Molecular Dynamics Options
==========================

========================    ============= ========  =====================================================================      ============================
Input variable              Variable type Required  Default                                                                    Value/Options/Notes
========================    ============= ========  =====================================================================      ============================
``MD_STYLE          =``     str           Y         None                                                                       Iterative MD method. Options are "CHIMES" (used for ChIMES model development) or "DFTB" (used when generating ChIMES corrections to DFTB).
``DFTB_MD_SER       =``     str           N         None                                                                       Only used when ``MD_STYLE`` set to "DFTB". DFTBplus executable absolute path.
``CHIMES_MD_MPI     =``     str           N         ``CHIMES_SRCDIR`` + "chimes_md-mpi"                                        Only used when ``MD_STYLE`` set to "CHIMES". MPI-compatible ChIMES_md exectuable absolute path.
``CHIMES_MD_SER     =``     str           N         ``CHIMES_SRCDIR`` + "chimes_md-serial"                                     Used when ``MD_STYLE`` set to either "CHIMES" or "DFTB*". Serial ChIMES_md executable absolute path. (See note below)
``MD_NODES          =``     list of int   N         [4] * ``NO_CASES``                                                         Number of nodes to use for MD jobs at each case. Number can be different for each case (e.g., [2,2,4,8] for four cases).
``MD_QUEUE          =``     list of str   N         ["pbatch"] * ``NO_CASES``                                                  Queue type to use for MD jobs at each case. Can be different for each case.
``MD_TIME           =``     list of str   N         ["4:00:00"] * ``NO_CASES``                                                 Walltime to use for MD jobs at each case. Can be different for each case.
``MDFILES           =``     str           N         ``WORKING_DIR`` + "ALL_BASE_FILES/CHIMESMD_BASEFILES/"                     Absolute path to MD input files like case-0.indep-0.run_md.in
``MD_MPI            =``     str           Y          None                                                                      MPI-compatible MD exectuable absolute path (either path to \"lmp_mpi_chimes\" or \"chimes_md-mpi\"). 
``MD_SER            =``     str           N         ``MD_MPI``                                                                 Serial MD executable absolute path (either LAMMPS path or CHIMES_MD_SER).
``CHIMES_MD_MODULES =``     str           N         cmake/3.21.1 + intel-classic/2021.6.0-magic + mvapich2/2.3.7 + mkl         System-specific modules needed to run ChIMES MD jobs.
``CHIMES_PEN_PREFAC =``     float         N         1.0E6                                                                      ChIMES penalty function prefactor.
``CHIMES_PEN_DIST   =``     float         N         0.02                                                                       ChIMES pentalty function kick-in distance
``MOLANAL           =``     str           N         None                                                                       Absolute path to molanal executable.
``LMP_FILES         =``     int           N         ``QM_FILES``                                                               Path to input files if using it as a reference (\"QM\") method.
``LMP_NODES         =``     int           N         1                                                                          Number of nodes to use for LAMMPS jobs.
``LMP_POSTPRC       =``     str           N         ``DRIVER_DIR`` + "/src/lmp_to_xyz.py"                                      Path to lmp2xyz.py
``LMP_PPN           =``     int           N         1                                                                          Number of procs per node to use for LAMMPS jobs.
``LMP_TIME          =``     str           N         ["00:30:00"]                                                               Walltime for LAMMPS calculations (HH:MM:SS).
``LMP_QUEUE         =``     str           N         "pdebug"                                                                   Queue to submit LAMMPS jobs to.
``LMP_EXE           =``     str           N         None                                                                       Absolute path to LAMMPS executable.
``LMP_MODULES       =``     str           N         None                                                                       System-specific modules needed to run LAMMPS.
``LMP_MEM           =``     str           N         ""                                                                         Memory requirements for running LAMMPS jobs.
``LMP_UNITS         =``     str           N         ``REAL``                                                                   Units LAMMPS input/output is expected to be.
========================    ============= ========  =====================================================================      ============================

.. Note ::

* ``CHIMES_MD_SER`` is used for old i/o based ChIMES/DFTB linking - update required, but needs bad_cfg printing in DFTB+ (requires change to interface)

===========================
Correction Fitting Options
===========================

=============================   =============  ========  ====================    ============================
Input variable                  Variable type  Required  Default                 Value/Options/Notes
=============================   =============  ========  ====================    ============================
``FIT_CORRECTION          =``   bool           N         False                   Is this ChIMES model being fit as a correction to another method?
``CORRECTED_TYPE          =``   str            N         None                    Method type being corrected. Currently only "DFTB" is supported
``CORRECTED_TYPE_FILES    =``   list of str    N         None                    List of parameter files needed to run simulations/single points with the method to be corrected 
``CORRECTED_TYPE_EXE      =``   str            N         None                    Executable to use when subtracting existing forces/energies/stresses from method to be corrected
``CORRECTED_TEMPS_BY_FILE =``   bool           N         False                   Should electron temperatures be set to values in traj_list.dat (false) or in specified file location, for correction calculation? Only needed if correction method is QM-based. See notes below.
=============================   =============  ========  ====================    ============================

.. Note ::

    Note: If corrections are used, ``ChIMES_MD_{NODES,QUEUE,TIME}`` are all used to specify DFTB runs. These should be renamed to ``simulation_{...}`` for the generalized MD block (which should become SIM block). 

    Note: If ``CORRECTED_TEMPS_BY_FILE`` is set to be ``True`` , temperaturess in ``traj_list.dat`` are ignored by correction FES subtraction. Instead, each training trajectory file in ``ALL_BASE_FILES/ALC-0_BASEFILES`` needs a corresponding .temps file that gives the temperature for each frame 


============================
Hierarchical Fitting Options
============================


=============================   =============   ====================    ============================
Input variable                  Variable type   Default                 Value/Options/Notes
=============================   =============   ====================    ============================
``DO_HIERARCH          =``      bool            False                   Is this a hierarchical fit (i.e., building on existing parameters?")
``HIERARCH_PARAM_FILES =``      list of str     None                    List of parameter files to build on, which should be in ALL_BASE_FILES/HIERARCH_PARAMS
``HIERARCH_METHOD      =``      str             None                      MD method to use for subtracting existing parameter contributions - current options are CHIMES or LMP
``HIERARCH_EXE         =``      str             None                    Executable to use when subtracting existing parameter contributions
=============================   =============   ====================    ============================


=================================
Reference QM Method Options
=================================


=============================   =============   =============================================   ============================
Input variable                  Variable type   Default                                         Value/Options/Notes
=============================   =============   =============================================   ============================
``QM_FILES       =``            str             WORKING_DIR + "ALL_BASE_FILES/VASP_BASEFILES"   Absolute path to QM input files generic to all QM methods. Can specify separately if multiple methods are being used (see code-specific options below)
``BULK_QM_METHOD =``            str             VASP                                            Specifies which nominal QM code to use for bulk configurations; options are "VASP" or "DFTB+"
``IGAS_QM_METHOD =``            int             VASP                                            Specifies which nominal QM code to use for gas configurations; options are "VASP", "DFTB+", and "Gaussian"
=============================   =============   =============================================   ============================

---------------------
VASP-Specific Options
---------------------

=============================   =============   ================================================    ============================
Input variable                  Variable type   Default                                             Value/Options/Notes
=============================   =============   ================================================    ============================
``VASP_NODES   =``              int             6                                                   Number of nodes to use for VASP jobs
``VASP_PPN     =``              int             ``HPC_PPN``                                         Number of processors to use per node for VASP jobs
``VASP_TIME    =``              str             "04:00:00"                                          Walltime for VASP calculations (HH:MM:SS)
``VASP_QUEUE   =``              str             "pbatch"                                            Queue to submit VASP jobs to
``VASP_EXE     =``              str             None                                                A path to a VASP executable **must** be specified if ``BULK_QM_METHOD`` or ``IGAS_QM_METHOD`` are set to "VASP"
``VASP_MODULES =``              str             "mkl"                                               Modules to load during VASP run
``VASP_POSTPRC =``              str             ``DRIVER_DIR`` + "/src/vasp2xyzf.py"                Absolute path to vasp2yzf.py
``VASP_MEM =``                  str             ""                                                  Memory requirements for running VASP jobs
=============================   =============   ================================================    ============================

------------------------
DFTB+ -Specific Options
------------------------

=============================   =============   =============================================================    ============================
Input variable                  Variable type   Default                                                          Value/Options/Notes
=============================   =============   =============================================================    ============================
``DFTB_FILES   =``              str             ``QM_FILES``                                                     Absolute path to DFTB+ input files.
``DFTB_NODES   =``              int             1                                                                Number of nodes to use for VASP jobs
``DFTB_PPN     =``              int             1                                                                Number of processors to use per node for VASP jobs
``DFTB_TIME    =``              str             "04:00:00"                                                       Walltime for VASP calculations (HH:MM:SS)
``DFTB_QUEUE   =``              str             "pbatch"                                                         Queue to submit VASP jobs to
``DFTB_EXE     =``              str             None                                                             A path to a VASP executable **must** be specified if ``BULK_QM_METHOD`` or ``IGAS_QM_METHOD`` are set to "DFTB+"
``DFTB_MODULES =``              str             "mkl"                                                            Modules to load during VASP run
``DFTB_MEM     =``              str             ""                                                               Memory requirements for running DFTB+ jobs
``DFTB_POST_PROC =``            str             "user_config.CHIMES_SRCDIR + "/../contrib/dftbgen_to_xyz.py"     Absolute path to dftgen_to_xyz.py 
=============================   =============   =============================================================    ============================

---------------------
CP2K-Specific Options
---------------------

=============================   =============    ================================================    ============================
Input variable                  Variable type    Default                                             Value/Options/Notes
=============================   =============    ================================================    ============================
``CP2K_NODES   =``              int              6                                                   Number of nodes to use for CP2K jobs
``CP2K_PPN     =``              int              ``HPC_PPN``                                         Number of processors to use per node for CP2K jobs
``CP2K_TIME    =``              str              "04:00:00"                                          Walltime for CP2K calculations (HH:MM:SS)
``CP2K_QUEUE   =``              str              "pbatch"                                            Queue to submit CP2K jobs to
``CP2K_EXE     =``              str              None                                                A path to a CP2K executable **must** be specified if ``BULK_QM_METHOD`` or ``IGAS_QM_METHOD`` are set to "CP2K"
``CP2K_MODULES =``              str              "mkl"                                               Modules to load during CP2K run
``CP2K_POSTPRC =``              str              user_config.DRIVER_DIR + "/src/cp2k_to_xyz.py"      Absolute path to CP2K2yzf.py
``CP2K_MEM =``                  str              ""                                                  Memory requirements for running CP2K jobs
``CP2K_DATDIR =``               str              None                                                Path to the directory containing potential and functional files for CP2K
=============================   =============    ================================================    ============================


--------------------------
Gaussian-Specific Options
--------------------------

=============================   =============   ====================    ============================
Input variable                  Variable type   Default                 Value/Options/Notes
=============================   =============   ====================    ============================
``GAUS_NODES =``                int             4                       Number of nodes to use for Gaussian jobs
``GAUS_PPN   =``                int             ``HPC_PPN``             Number of processors to use per node for Gaussian jobs
``GAUS_TIME  =``                str             "04:00:00"              Walltime for Gaussian calculations (HH:MM:SS)
``GAUS_QUEUE =``                str             "pbatch"                Queue to submit Gaussian jobs to
``GAUS_EXE   =``                str             None                    A path to a Gaussian executable **must** be specified if ``IGAS_QM_METHOD`` is set to "Gaussian"
``GAUS_SCR   =``                str             None                    Absolute path to Gaussian scratch directory
``GAUS_REF   =``                str             None                    Name of file containing single atom energies from Gaussian and target planewave method
``GAUS_MEM   =``                str             ""                      Memory requirements for running Gaussian jobs
=============================   =============   ====================    ============================

.. Note ::

    The file specified for ``GAUS_REF`` is structured like:

    .. code-block :: text

        <chemical symbol> <Gaussian energy> <planewave code energy>
        <chemical symbol> <Gaussian energy> <planewave code energy>
        <chemical symbol> <Gaussian energy> <planewave code energy>
        ...
        <chemical symbol> <Gaussian energy> <planewave code energy>

    Energies are expected in kcal/mol and there should be an entry for each atom type of interest.





